from flask import Blueprint, request, jsonify
from models.student import Student
from models.event import Event
from models.attendance import Attendance
from models.unauthorized_log import UnauthorizedLog
from utils.qr_generator import QRGenerator
from utils.email_service import EmailService
from utils.sanitizer import InputSanitizer
import jwt
from config import Config
import json

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/scan', methods=['POST'])
def scan_qr():
    """Handle QR code scanning for attendance"""
    try:
        # Verify student token and get student_id
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'student':
                return jsonify({'success': False, 'message': 'Invalid token type'}), 401
            student_id = payload.get('student_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        data = request.get_json()
        qr_data_str = data.get('qr_data')
        
        if not qr_data_str:
            return jsonify({'success': False, 'message': 'QR code data is required'}), 400
        
        # Verify and parse QR code
        qr_data, error = QRGenerator.verify_qr_data(qr_data_str)
        
        if error:
            return jsonify({'success': False, 'message': error}), 400
        
        event_id = qr_data['event_id']
        secure_token = qr_data['secure_token']
        
        # Verify student exists
        student = Student.find_by_id(student_id)
        if not student:
            # Log unauthorized scan
            UnauthorizedLog.log_unauthorized_scan(
                qr_token=secure_token,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                scan_data={'student_id': student_id, 'event_id': event_id}
            )
            return jsonify({'success': False, 'message': 'Student not found. Unauthorized scan logged.'}), 404
        
        # Verify event exists
        event = Event.find_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        # Check if student registered for this event
        registered_events = student.get('registered_events', [])
        # Handle both MongoDB ObjectIds and Supabase string IDs
        registered_event_ids = []
        for eid in registered_events:
            if isinstance(eid, str):
                registered_event_ids.append(eid)
            else:
                registered_event_ids.append(str(eid))
        
        if event_id not in registered_event_ids:
            # Log unauthorized scan
            UnauthorizedLog.log_unauthorized_scan(
                qr_token=secure_token,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                scan_data={
                    'student_id': student_id,
                    'student_name': student['name'],
                    'event_id': event_id,
                    'event_name': event['event_name'],
                    'reason': 'Student not registered for event'
                }
            )
            return jsonify({
                'success': False,
                'message': f'You are not registered for {event["event_name"]}. Unauthorized scan logged.'
            }), 403
        
        # Check if attendance already marked
        existing_attendance = Attendance.check_attendance(student_id, event_id)
        if existing_attendance:
            # Handle both datetime objects (MongoDB) and ISO strings (Supabase)
            marked_at = existing_attendance['marked_at']
            if hasattr(marked_at, 'isoformat'):
                marked_at_str = marked_at.isoformat()
            else:
                marked_at_str = marked_at
                
            return jsonify({
                'success': False,
                'message': 'Attendance already recorded for this event.',
                'marked_at': marked_at_str
            }), 400
        
        # Mark attendance
        attendance_id = Attendance.mark_attendance(student_id, event_id, secure_token)
        
        # Send confirmation email
        try:
            EmailService.send_attendance_confirmation(
                student['email'],
                student['name'],
                event['event_name']
            )
        except Exception as e:
            print(f"Email notification failed: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': f'Attendance marked successfully for {event["event_name"]}!',
            'attendance_id': str(attendance_id),
            'student_name': student['name'],
            'event_name': event['event_name']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Attendance marking failed: {str(e)}'}), 500


@attendance_bp.route('/verify-qr', methods=['POST'])
def verify_qr():
    """Verify QR code without marking attendance"""
    try:
        data = request.get_json()
        qr_data_str = data.get('qr_data')
        
        if not qr_data_str:
            return jsonify({'success': False, 'message': 'QR code data is required'}), 400
        
        # Verify and parse QR code
        qr_data, error = QRGenerator.verify_qr_data(qr_data_str)
        
        if error:
            return jsonify({'success': False, 'message': error}), 400
        
        event_id = qr_data['event_id']
        
        # Get event details
        event = Event.find_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'message': 'Event not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'QR code is valid',
            'event': {
                'id': InputSanitizer.get_id(event),
                'event_name': event['event_name'],
                'description': event['description'],
                'date': event['date'],
                'venue': event['venue']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'QR verification failed: {str(e)}'}), 500


@attendance_bp.route('/my-attendance', methods=['GET'])
def get_my_attendance():
    """Get student's attendance records"""
    try:
        student_id = request.args.get('student_id')
        
        if not student_id:
            return jsonify({'success': False, 'message': 'Student ID is required'}), 400
        
        # Verify student exists
        student = Student.find_by_id(student_id)
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Get attendance records
        attendance_records = Attendance.get_student_attendance(student_id)
        
        # Get detailed information
        attendance_list = []
        for record in attendance_records:
            event_id_str = str(record['event_id'])
            event = Event.find_by_id(event_id_str)
            if event:
                # Handle both datetime objects (MongoDB) and ISO strings (Supabase)
                marked_at = record['marked_at']
                if hasattr(marked_at, 'isoformat'):
                    marked_at_iso = marked_at.isoformat()
                else:
                    marked_at_iso = marked_at
                
                attendance_list.append({
                    'event_id': InputSanitizer.get_id(event),
                    'event_name': event['event_name'],
                    'marked_at': marked_at_iso,
                    'status': record['status']
                })
        
        return jsonify({
            'success': True,
            'total_attended': len(attendance_list),
            'attendance': attendance_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to fetch attendance: {str(e)}'}), 500

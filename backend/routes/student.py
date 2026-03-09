from flask import Blueprint, request, jsonify
from models.student import Student
from models.event import Event
from utils.email_service import EmailService
from utils.sanitizer import InputSanitizer
import jwt
from config import Config

student_bp = Blueprint('student', __name__)

def verify_student_token(token):
    """Verify student JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        if payload.get('type') != 'student':
            return None, 'Invalid token type'
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'


@student_bp.route('/events', methods=['GET'])
def get_events():
    """Get all available events"""
    try:
        events = Event.get_all_events()
        
        events_list = []
        for event in events:
            events_list.append({
                'id': InputSanitizer.get_id(event),
                'event_name': event['event_name'],
                'description': event['description'],
                'date': event['date'],
                'venue': event['venue'],
                'max_participants': event.get('max_participants'),
                'total_registered': event.get('total_registered', 0)
            })
        
        return jsonify({
            'success': True,
            'events': events_list
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to fetch events: {str(e)}'}), 500


@student_bp.route('/register-events', methods=['POST'])
def register_events():
    """Register student for ONE event (enforced)"""
    try:
        # Verify token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        payload, error = verify_student_token(token)
        
        if error:
            return jsonify({'success': False, 'message': error}), 401
        
        student_id = payload['student_id']
        
        # Check if student is already registered for an event
        student = Student.find_by_id(student_id)
        if student and len(student.get('registered_events', [])) > 0:
            return jsonify({'success': False, 'message': 'You have already registered for an event'}), 400
        
        data = request.get_json()
        event_ids = data.get('event_ids', [])
        
        if not event_ids:
            return jsonify({'success': False, 'message': 'Please select an event'}), 400
        
        # Enforce single event registration
        if len(event_ids) > 1:
            return jsonify({'success': False, 'message': 'You can only register for ONE event'}), 400
        
        # Validate event ID
        event_id = event_ids[0]
        event = Event.find_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'message': f'Invalid event ID: {event_id}'}), 400
        
        # Update student's registered events
        Student.update_registered_events(student_id, event_ids)
        
        # Update event registration count
        Event.update_registration_count(event_id, 1)
        
        # Get event details for email
        event_names = [event['event_name']]
        
        # Send confirmation email
        try:
            EmailService.send_registration_confirmation(
                student['email'],
                student['name'],
                event_names
            )
        except Exception as e:
            print(f"Email notification failed: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': 'Event registered successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500


@student_bp.route('/my-events', methods=['GET'])
def get_my_events():
    """Get student's registered events"""
    try:
        # Verify token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        payload, error = verify_student_token(token)
        
        if error:
            return jsonify({'success': False, 'message': error}), 401
        
        student_id = payload['student_id']
        student = Student.find_by_id(student_id)
        
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Get event details
        registered_events = []
        for event_id in student.get('registered_events', []):
            event = Event.find_by_id(event_id)
            if event:
                registered_events.append({
                    'id': InputSanitizer.get_id(event),
                    'event_name': event['event_name'],
                    'description': event['description'],
                    'date': event['date'],
                    'venue': event['venue']
                })
        
        return jsonify({
            'success': True,
            'events': registered_events
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to fetch events: {str(e)}'}), 500


@student_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get student profile"""
    try:
        # Verify token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        payload, error = verify_student_token(token)
        
        if error:
            return jsonify({'success': False, 'message': error}), 401
        
        student_id = payload['student_id']
        student = Student.find_by_id(student_id)
        
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        return jsonify({
            'success': True,
            'student': {
                'id': InputSanitizer.get_id(student),
                'name': student['name'],
                'register_number': student['register_number'],
                'department': student['department'],
                'course': student.get('course', 'N/A'),
                'year': student['year'],
                'email': student['email'],
                'phone_number': student['phone_number'],
                'registered_events_count': len(student.get('registered_events', []))
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to fetch profile: {str(e)}'}), 500


@student_bp.route('/search/<register_number>', methods=['GET'])
def search_by_register_number(register_number):
    """Search student by register number (requires admin token)"""
    try:
        # Verify admin token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'admin':
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
        except:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        student = Student.find_by_register_number(register_number)
        
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        # Get registered events
        registered_events = []
        for event_id in student.get('registered_events', []):
            event = Event.find_by_id(event_id)
            if event:
                registered_events.append({
                    'id': InputSanitizer.get_id(event),
                    'event_name': event['event_name']
                })
        
        return jsonify({
            'success': True,
            'student': {
                'id': InputSanitizer.get_id(student),
                'name': student['name'],
                'register_number': student['register_number'],
                'department': student['department'],
                'course': student.get('course', 'N/A'),
                'year': student['year'],
                'email': student['email'],
                'phone_number': student['phone_number'],
                'registered_events': registered_events
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Search failed: {str(e)}'}), 500

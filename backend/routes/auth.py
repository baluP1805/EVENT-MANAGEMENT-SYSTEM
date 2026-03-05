from flask import Blueprint, request, jsonify
from models.student import Student
from utils.validators import Validators
from utils.sanitizer import InputSanitizer
from utils.email_service import EmailService
import jwt
from config import Config
from datetime import datetime, timedelta
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Student registration endpoint"""
    try:
        data = request.get_json()
        
        # Sanitize inputs
        allowed_keys = ['name', 'register_number', 'department', 'course', 'year', 'email', 'phone_number', 'password']
        data = InputSanitizer.sanitize_dict(data, allowed_keys)
        
        # Extract and validate data
        name = InputSanitizer.sanitize_name(data.get('name', ''))
        register_number = InputSanitizer.sanitize_register_number(data.get('register_number', ''))
        department = data.get('department', '').strip()
        course = data.get('course', '').strip()
        year = data.get('year', '').strip()
        email = InputSanitizer.sanitize_email(data.get('email', ''))
        phone_number = InputSanitizer.sanitize_phone(data.get('phone_number', ''))
        password = data.get('password', '')
        
        # Validate inputs
        valid, error = Validators.validate_name(name)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_register_number(register_number)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_department(department)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_course(course)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_year(year)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_email(email)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_phone_number(phone_number)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        valid, error = Validators.validate_password(password)
        if not valid:
            return jsonify({'success': False, 'message': error}), 400
        
        # Check for duplicate email
        existing_student = Student.find_by_email(email)
        if existing_student:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Check for duplicate register number
        existing_register = Student.find_by_register_number(register_number)
        if existing_register:
            return jsonify({'success': False, 'message': 'Register number already exists'}), 400
        
        # Create student
        student_id = Student.create(
            name=Validators.sanitize_input(name),
            register_number=Validators.sanitize_input(register_number),
            department=Validators.sanitize_input(department),
            course=Validators.sanitize_input(course),
            year=year,
            email=email.lower(),
            phone_number=phone_number,
            password=password
        )
        
        # Send welcome email
        try:
            EmailService.send_welcome_email(
                email.lower(),
                Validators.sanitize_input(name),
                Validators.sanitize_input(register_number)
            )
        except Exception as email_err:
            pass  # Email failure must not block registration

        return jsonify({
            'success': True,
            'message': 'Registration successful! Please login.',
            'student_id': str(student_id)
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Student login endpoint"""
    try:
        data = request.get_json()
        
        # Sanitize inputs
        email = InputSanitizer.sanitize_email(data.get('email', ''))
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Find student
        student = Student.find_by_email(email)
        if not student:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Verify password
        if not Student.verify_password(student['password'], password):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'student_id': InputSanitizer.get_id(student),
            'email': student['email'],
            'type': 'student',
            'exp': datetime.utcnow() + Config.JWT_EXPIRATION
        }, Config.JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'student': {
                'id': InputSanitizer.get_id(student),
                'name': student['name'],
                'email': student['email'],
                'register_number': student['register_number'],
                'department': student['department'],
                'year': student['year']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        
        # Sanitize inputs
        email = InputSanitizer.sanitize_email(data.get('email', ''))
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Verify admin credentials
        if email == Config.ADMIN_EMAIL and password == Config.ADMIN_PASSWORD:
            # Generate JWT token
            token = jwt.encode({
                'email': email,
                'type': 'admin',
                'exp': datetime.utcnow() + Config.JWT_EXPIRATION
            }, Config.JWT_SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'success': True,
                'message': 'Admin login successful',
                'token': token,
                'admin': {
                    'email': email,
                    'role': 'admin'
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid admin credentials'}), 401
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Admin login failed: {str(e)}'}), 500


@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify JWT token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'success': False, 'message': 'No token provided'}), 401
        
        # Decode token
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        
        return jsonify({
            'success': True,
            'payload': payload
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401

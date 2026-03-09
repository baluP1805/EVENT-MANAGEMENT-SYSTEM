import re
import validators

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False, 'Email is required'
        
        if not validators.email(email):
            return False, 'Invalid email format'
        
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or not isinstance(password, str):
            return False, 'Password is required'
        
        if len(password) < 6:
            return False, 'Password must be at least 6 characters long'
        
        # Check for at least one letter and one number
        if not re.search('[a-zA-Z]', password) or not re.search('[0-9]', password):
            return False, 'Password must contain at least one letter and one number'
        
        return True, None
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate phone number format"""
        if not phone or not isinstance(phone, str):
            return False, 'Phone number is required'
        
        # Remove spaces and dashes
        phone_cleaned = re.sub(r'[\s\-]', '', phone)
        
        # Check if it's a valid phone number (10 digits for Indian numbers)
        if not re.match(r'^[6-9]\d{9}$', phone_cleaned):
            return False, 'Invalid phone number format. Must be 10 digits starting with 6-9'
        
        return True, None
    
    @staticmethod
    def validate_register_number(register_number):
        """Validate register number format"""
        if not register_number or not isinstance(register_number, str):
            return False, 'Register number is required'
        
        if len(register_number) < 3:
            return False, 'Register number must be at least 3 characters'
        
        return True, None
    
    @staticmethod
    def validate_name(name):
        """Validate name"""
        if not name or not isinstance(name, str):
            return False, 'Name is required'
        
        if len(name.strip()) < 2:
            return False, 'Name must be at least 2 characters'
        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False, 'Name can only contain letters and spaces'
        
        return True, None
    
    @staticmethod
    def validate_department(department):
        """Validate department"""
        valid_departments = ['Management', 'Science', 'Arts']
        
        if not department or not isinstance(department, str):
            return False, 'Department is required'
        
        if department not in valid_departments:
            return False, f'Department must be one of: {", ".join(valid_departments)}'
        
        return True, None
    
    @staticmethod
    def validate_course(course):
        """Validate course/programme"""
        if not course or not isinstance(course, str):
            return False, 'Course/Programme is required'
        
        if len(course.strip()) < 3:
            return False, 'Course name must be at least 3 characters'
        
        return True, None
    
    @staticmethod
    def validate_year(year):
        """Validate year"""
        if not year or not isinstance(year, str):
            return False, 'Year is required'
        
        valid_years = ['1st Year', '2nd Year', '3rd Year', '4th Year']
        
        if year not in valid_years:
            return False, f'Year must be one of: {", ".join(valid_years)}'
        
        return True, None
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize user input to prevent XSS"""
        if not text or not isinstance(text, str):
            return text
        
        # Remove potentially dangerous characters
        text = text.strip()
        text = re.sub(r'[<>\"\'&]', '', text)
        
        return text

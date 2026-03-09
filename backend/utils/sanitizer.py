"""
Input Sanitization Utilities
Prevents XSS, SQL injection, and malicious input
"""
import re
import html
from typing import Any, Dict, List, Union

class InputSanitizer:
    """Sanitize user inputs to prevent security vulnerabilities"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 500) -> str:
        """
        Sanitize string input by:
        - Escaping HTML entities
        - Removing potentially dangerous characters
        - Limiting length
        """
        if not isinstance(value, str):
            return ""
        
        # Escape HTML entities
        sanitized = html.escape(value.strip())
        
        # Remove null bytes and other control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        # Limit length
        sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Validate and sanitize email addresses
        """
        if not isinstance(email, str):
            return ""
        
        email = email.strip().lower()
        
        # Basic email pattern validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email[:254]  # Max email length per RFC
    
    @staticmethod
    def sanitize_register_number(reg_num: str) -> str:
        """
        Sanitize registration numbers (alphanumeric only)
        """
        if not isinstance(reg_num, str):
            return ""
        
        # Allow only alphanumeric and hyphens
        sanitized = re.sub(r'[^a-zA-Z0-9-]', '', reg_num.strip().upper())
        
        return sanitized[:50]
    
    @staticmethod
    def sanitize_phone(phone: str) -> str:
        """
        Sanitize phone numbers (digits, spaces, +, -, () only)
        """
        if not isinstance(phone, str):
            return ""
        
        # Allow only digits and common phone formatting characters
        sanitized = re.sub(r'[^0-9+\-() ]', '', phone.strip())
        
        return sanitized[:20]
    
    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Sanitize names (letters, spaces, hyphens, apostrophes only)
        """
        if not isinstance(name, str):
            return ""
        
        # Allow letters, spaces, hyphens, apostrophes
        sanitized = re.sub(r'[^a-zA-Z\s\'-]', '', name.strip())
        
        # Remove multiple spaces
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized[:100]
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """
        Sanitize dictionary by:
        - Removing unexpected keys
        - Sanitizing values based on type
        """
        sanitized = {}
        
        for key in allowed_keys:
            if key not in data:
                continue
            
            value = data[key]
            
            if isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, (int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, list):
                # Sanitize list items if they're strings
                sanitized[key] = [
                    InputSanitizer.sanitize_string(item) if isinstance(item, str) else item
                    for item in value
                ]
            elif isinstance(value, dict):
                # Recursively sanitize nested dictionaries
                sanitized[key] = {
                    k: InputSanitizer.sanitize_string(v) if isinstance(v, str) else v
                    for k, v in value.items()
                }
        
        return sanitized
    
    @staticmethod
    def validate_object_id(oid: str) -> bool:
        """
        Validate MongoDB ObjectId format
        """
        return bool(re.match(r'^[a-f0-9]{24}$', oid))
    
    @staticmethod
    def get_id(obj: Dict) -> str:
        """
        Get ID from either Supabase (id field) or MongoDB (_id field)
        Works with both database backends seamlessly
        """
        if not isinstance(obj, dict):
            return ""
        
        # Try Supabase first (id field)
        if 'id' in obj and obj['id']:
            return str(obj['id'])
        
        # Fall back to MongoDB (_id field)
        if '_id' in obj and obj['_id']:
            return str(obj['_id'])
        
        # No valid ID found
        return ""
    
    @staticmethod
    def sanitize_search_query(query: str) -> str:
        """
        Sanitize search queries to prevent injection attacks
        """
        if not isinstance(query, str):
            return ""
        
        # Escape special regex characters that could be used in MongoDB queries
        dangerous_chars = ['$', '{', '}', '\\', '|', '^']
        sanitized = query.strip()
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized[:200]


# Decorator for route input sanitization
def sanitize_input(allowed_keys: List[str] = None):
    """
    Decorator to sanitize request JSON input
    """
    from functools import wraps
    from flask import request, jsonify
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.is_json:
                data = request.get_json()
                
                if allowed_keys:
                    # Sanitize dict with allowed keys
                    sanitized_data = InputSanitizer.sanitize_dict(data, allowed_keys)
                    request.sanitized_data = sanitized_data
                else:
                    # Basic sanitization for all string values
                    request.sanitized_data = {
                        k: InputSanitizer.sanitize_string(v) if isinstance(v, str) else v
                        for k, v in data.items()
                    }
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator

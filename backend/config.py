import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

    # Supabase (sole database backend)
    USE_SUPABASE = True
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_EXPIRATION = timedelta(hours=24)
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    # From address must match authenticated Gmail; fall back to MAIL_USERNAME automatically
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '') or os.getenv('MAIL_USERNAME', '')
    
    # Admin Credentials (default admin - should be changed)
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@college.edu')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Admin@123')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    
    # QR Code Settings
    QR_CODE_EXPIRY_HOURS = 24
    
    # File Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

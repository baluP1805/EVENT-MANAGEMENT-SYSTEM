import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # MongoDB
    # Allow either a full URI that includes a database or a separate DATABASE_NAME
    raw_mongo = os.getenv('MONGO_URI', '')
    # Normalize trailing slash
    if raw_mongo and raw_mongo.endswith('/'):
        raw_mongo = raw_mongo[:-1]
    MONGO_URI = raw_mongo
    # If DATABASE_NAME not provided, try to infer from the URI path, else fallback
    DATABASE_NAME = os.getenv('DATABASE_NAME') or (raw_mongo.split('/')[-1] if raw_mongo and '/' in raw_mongo and raw_mongo.split('/')[-1] else 'college_ems')

    # Supabase / Postgres
    # NOTE: Supabase project URL should be a full URL (https://<ref>.supabase.co).
    # The user provided an anon key; SUPABASE_URL must still be supplied to connect.
    USE_SUPABASE = os.getenv('USE_SUPABASE', 'true').lower() in ('1', 'true', 'yes')
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    # Supabase anon/service key provided by user — stored here as default for immediate configuration
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsY2dmYnZhZHNkYWVjend0bmdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTc2NjMsImV4cCI6MjA4ODI5MzY2M30.3FEOtoUcCRI_hW_2UNTaFwnnRVBcnXbDPdu9ijK9Xms')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_EXPIRATION = timedelta(hours=24)
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@collegeems.com')
    
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

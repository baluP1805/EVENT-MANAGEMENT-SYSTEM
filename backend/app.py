from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from dotenv import load_dotenv
import os
load_dotenv()
from config import Config
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.attendance import attendance_bp
from models.event import Event
import logging

# Detect Vercel serverless environment
IS_VERCEL = os.getenv('VERCEL') == '1' or os.getenv('VERCEL_ENV') is not None

# Resolve frontend static folder — works both locally and on Vercel
_here = os.path.dirname(os.path.abspath(__file__))
_frontend = os.path.join(_here, '..', 'frontend')
if not os.path.isdir(_frontend):
    _frontend = os.path.join(_here, 'frontend')  # fallback

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.abspath(_frontend), static_url_path='')
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Security headers with Talisman — skip on Vercel (serverless HTTPS is handled by the platform)
if os.getenv('FLASK_ENV') == 'production' and not IS_VERCEL:
    csp = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "cdn.jsdelivr.net", "unpkg.com"],
        'style-src': ["'self'", "'unsafe-inline'", "fonts.googleapis.com", "cdnjs.cloudflare.com"],
        'font-src': ["'self'", "fonts.gstatic.com", "cdnjs.cloudflare.com"],
        'img-src': ["'self'", "data:", "blob:"],
        'connect-src': ["'self'"]
    }
    Talisman(app,
        force_https=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        frame_options='DENY',
        frame_options_allow_from=None,
        referrer_policy='strict-origin-when-cross-origin',
        feature_policy={
            'geolocation': "'none'",
            'camera': "'self'",
            'microphone': "'none'"
        }
    )
    logging.info("Security headers enabled (Talisman)")
else:
    logging.info("Talisman disabled (development or Vercel)")

# Initialize rate limiter — use memory:// which is fine for serverless cold starts
try:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=Config.RATELIMIT_STORAGE_URL,
        default_limits=["200 per day", "50 per hour"]
    )
except Exception as _limiter_err:
    logging.warning(f"Rate limiter init failed (non-fatal): {_limiter_err}")
    limiter = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

# Initialize default events
with app.app_context():
    try:
        Event.initialize_default_events()
        logger.info("Default events initialized")
    except Exception as e:
        logger.error(f"Error initializing default events: {str(e)}")

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'College EMS API is running'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({'success': False, 'message': 'Rate limit exceeded. Please try again later.'}), 429

if __name__ == '__main__':
    logger.info("Starting College Event Management System...")
    app.run(debug=True, host='0.0.0.0', port=5000)

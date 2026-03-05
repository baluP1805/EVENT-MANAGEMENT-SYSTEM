from flask import Blueprint

# Initialize blueprints
auth_bp = Blueprint('auth', __name__)
student_bp = Blueprint('student', __name__)
admin_bp = Blueprint('admin', __name__)
attendance_bp = Blueprint('attendance', __name__)

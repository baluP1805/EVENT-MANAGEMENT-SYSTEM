import bcrypt
from datetime import datetime
from supabase_client import get_supabase_client


class Student:
    @staticmethod
    def create(name, register_number, department, course, year, email, phone_number, password):
        """Create a new student in Supabase."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        created_at = datetime.utcnow().isoformat()
        sb = get_supabase_client()
        payload = {
            'name': name,
            'register_number': register_number,
            'department': department,
            'course': course,
            'year': year,
            'email': email.lower(),
            'phone_number': phone_number,
            'password': hashed_password,
            'registered_events': [],
            'created_at': created_at,
            'updated_at': created_at
        }
        try:
            res = sb.table('students').insert(payload).execute()
            return res.data[0].get('id')
        except Exception as e:
            raise RuntimeError('Failed to insert student into Supabase: ' + str(e))

    @staticmethod
    def find_by_email(email):
        """Find student by email."""
        sb = get_supabase_client()
        res = sb.table('students').select('*').eq('email', email.lower()).limit(1).execute()
        return res.data[0] if res.data else None

    @staticmethod
    def find_by_id(student_id):
        """Find student by ID."""
        sb = get_supabase_client()
        res = sb.table('students').select('*').eq('id', student_id).limit(1).execute()
        return res.data[0] if res.data else None

    @staticmethod
    def find_by_register_number(register_number):
        """Find student by register number."""
        sb = get_supabase_client()
        res = sb.table('students').select('*').eq('register_number', register_number).limit(1).execute()
        return res.data[0] if res.data else None

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify password."""
        stored = stored_password.encode('utf-8') if isinstance(stored_password, str) else stored_password
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored)

    @staticmethod
    def update_registered_events(student_id, event_ids):
        """Update student's registered events."""
        sb = get_supabase_client()
        payload = {'registered_events': event_ids, 'updated_at': datetime.utcnow().isoformat()}
        return sb.table('students').update(payload).eq('id', student_id).execute()

    @staticmethod
    def get_all_students():
        """Get all students."""
        sb = get_supabase_client()
        res = sb.table('students').select('*').execute()
        return res.data or []

    @staticmethod
    def count_students():
        """Count total students."""
        sb = get_supabase_client()
        res = sb.table('students').select('id').execute()
        return len(res.data) if res and res.data else 0

    @staticmethod
    def get_students_by_department():
        """Get student count grouped by department."""
        sb = get_supabase_client()
        res = sb.table('students').select('department').execute()
        counts = {}
        for s in (res.data or []):
            dept = s.get('department') or 'Unknown'
            counts[dept] = counts.get(dept, 0) + 1
        return sorted([{'department': k, 'count': v} for k, v in counts.items()], key=lambda x: -x['count'])

    @staticmethod
    def get_students_by_event(event_id):
        """Get all students registered for a specific event."""
        sb = get_supabase_client()
        res = sb.table('students').select('*').execute()
        filtered = []
        for student in (res.data or []):
            registered_events = student.get('registered_events') or []
            if isinstance(registered_events, list) and event_id in registered_events:
                filtered.append(student)
        return filtered

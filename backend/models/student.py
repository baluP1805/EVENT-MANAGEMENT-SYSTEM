from models import students_collection
from bson import ObjectId
import bcrypt
from datetime import datetime
from config import Config

# Optional Supabase support
if Config.USE_SUPABASE:
    from supabase_client import get_supabase_client


class Student:
    @staticmethod
    def create(name, register_number, department, course, year, email, phone_number, password):
        """Create a new student. Uses Supabase when enabled, otherwise MongoDB."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        created_at = datetime.utcnow()

        if Config.USE_SUPABASE:
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
                'created_at': created_at.isoformat(),
                'updated_at': created_at.isoformat()
            }
            try:
                res = sb.table('students').insert(payload).execute()
                return res.data[0].get('id')
            except Exception as e:
                raise RuntimeError('Failed to insert student into Supabase: ' + str(e))

        # MongoDB fallback
        student_data = {
            'name': name,
            'register_number': register_number,
            'department': department,
            'course': course,
            'year': year,
            'email': email.lower(),
            'phone_number': phone_number,
            'password': hashed_password.encode('utf-8'),
            'registered_events': [],
            'created_at': created_at,
            'updated_at': created_at
        }
        result = students_collection.insert_one(student_data)
        return result.inserted_id

    @staticmethod
    def find_by_email(email):
        """Find student by email"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('students').select('*').eq('email', email.lower()).limit(1).execute()
            if res.data:
                return res.data[0]
            return None

        return students_collection.find_one({'email': email.lower()})

    @staticmethod
    def find_by_id(student_id):
        """Find student by ID"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('students').select('*').eq('id', student_id).limit(1).execute()
            return res.data[0] if res.data else None

        return students_collection.find_one({'_id': ObjectId(student_id)})

    @staticmethod
    def find_by_register_number(register_number):
        """Find student by register number"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('students').select('*').eq('register_number', register_number).limit(1).execute()
            return res.data[0] if res.data else None

        return students_collection.find_one({'register_number': register_number})

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify password"""
        # stored_password for Supabase is a UTF-8 string, Mongo stores bytes
        if isinstance(stored_password, str):
            stored = stored_password.encode('utf-8')
        else:
            stored = stored_password
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored)

    @staticmethod
    def update_registered_events(student_id, event_ids):
        """Update student's registered events"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            payload = {'registered_events': event_ids, 'updated_at': datetime.utcnow().isoformat()}
            res = sb.table('students').update(payload).eq('id', student_id).execute()
            return res

        from bson import ObjectId
        event_objects = [ObjectId(eid) if isinstance(eid, str) else eid for eid in event_ids]
        return students_collection.update_one(
            {'_id': ObjectId(student_id)},
            {
                '$set': {
                    'registered_events': event_objects,
                    'updated_at': datetime.utcnow()
                }
            }
        )

    @staticmethod
    def get_all_students():
        """Get all students"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('students').select('*').execute()
            return res.data
        return list(students_collection.find())

    @staticmethod
    def count_students():
        """Count total students"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('students').select('id').execute()
            return len(res.data) if res and res.data else 0
        return students_collection.count_documents({})

    @staticmethod
    def get_students_by_department():
        """Get student count by department"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            # Supabase SQL view or RPC is recommended; using simple select and group here
            res = sb.table('students').select('department').execute()
            data = res.data or []
            counts = {}
            for s in data:
                dept = s.get('department') or 'Unknown'
                counts[dept] = counts.get(dept, 0) + 1
            return sorted([{'department': k, 'count': v} for k,v in counts.items()], key=lambda x: -x['count'])

        pipeline = [
            {
                '$group': {
                    '_id': '$department',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ]
        return list(students_collection.aggregate(pipeline))

    @staticmethod
    def get_students_by_event(event_id):
        """Get all students registered for a specific event"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            # Get all students and filter in Python to avoid JSONB parsing issues
            res = sb.table('students').select('*').execute()
            all_students = res.data or []
            
            # Filter students who have this event_id in their registered_events array
            filtered_students = []
            for student in all_students:
                registered_events = student.get('registered_events', [])
                # Handle both empty arrays and None
                if not registered_events:
                    continue
                # Handle JSONB array - registered_events should be a list
                if isinstance(registered_events, list) and event_id in registered_events:
                    filtered_students.append(student)
            
            return filtered_students

        from bson import ObjectId
        event_obj = ObjectId(event_id) if isinstance(event_id, str) else event_id
        return list(students_collection.find({
            '$or': [
                {'registered_events': event_obj},
                {'registered_events': str(event_obj)}
            ]
        }))

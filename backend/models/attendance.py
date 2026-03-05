from models import attendance_collection
from bson import ObjectId
from datetime import datetime
from config import Config

if Config.USE_SUPABASE:
    from supabase_client import get_supabase_client


class Attendance:
    @staticmethod
    def mark_attendance(student_id, event_id, qr_token):
        """Mark attendance for a student"""
        payload = {
            'student_id': student_id,
            'event_id': event_id,
            'qr_token': qr_token,
            'marked_at': datetime.utcnow().isoformat(),
            'status': 'present'
        }
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            try:
                res = sb.table('attendance').insert(payload).execute()
                return res.data[0].get('id')
            except Exception as e:
                raise RuntimeError('Failed to insert attendance into Supabase: ' + str(e))

        attendance_data = {
            'student_id': ObjectId(student_id),
            'event_id': ObjectId(event_id),
            'qr_token': qr_token,
            'marked_at': datetime.utcnow(),
            'status': 'present'
        }
        result = attendance_collection.insert_one(attendance_data)
        return result.inserted_id

    @staticmethod
    def check_attendance(student_id, event_id):
        """Check if attendance already marked"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('attendance').select('*').match({'student_id': student_id, 'event_id': event_id}).limit(1).execute()
            return res.data[0] if res.data else None

        return attendance_collection.find_one({
            'student_id': ObjectId(student_id),
            'event_id': ObjectId(event_id)
        })

    @staticmethod
    def get_event_attendance(event_id):
        """Get all attendance for an event"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('attendance').select('*').eq('event_id', event_id).execute()
            return res.data or []
        return list(attendance_collection.find({'event_id': ObjectId(event_id)}))

    @staticmethod
    def get_student_attendance(student_id):
        """Get all attendance for a student"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('attendance').select('*').eq('student_id', student_id).execute()
            return res.data or []
        return list(attendance_collection.find({'student_id': ObjectId(student_id)}))

    @staticmethod
    def count_event_attendance(event_id):
        """Count attendance for an event"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('attendance').select('id').eq('event_id', event_id).execute()
            return len(res.data) if res and res.data else 0
        return attendance_collection.count_documents({'event_id': ObjectId(event_id)})

    @staticmethod
    def get_attendance_by_event():
        """Get attendance count grouped by event"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('attendance').select('event_id').execute()
            data = res.data or []
            counts = {}
            for r in data:
                eid = r.get('event_id')
                counts[eid] = counts.get(eid, 0) + 1
            return [{'event_id': k, 'count': v} for k,v in counts.items()]

        pipeline = [
            {
                '$group': {
                    '_id': '$event_id',
                    'count': {'$sum': 1}
                }
            }
        ]
        return list(attendance_collection.aggregate(pipeline))

    @staticmethod
    def get_attendance_statistics():
        """Get comprehensive attendance statistics"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            # This is a simple join-like approach by fetching attendance and enriching in Python
            att_res = sb.table('attendance').select('*').execute()
            students_res = sb.table('students').select('*').execute()
            events_res = sb.table('events').select('*').execute()
            students = {s['id']: s for s in (students_res.data or [])}
            events = {e['id']: e for e in (events_res.data or [])}
            stats = {}
            for a in (att_res.data or []):
                ev = events.get(a.get('event_id'))
                st = students.get(a.get('student_id'))
                key = (a.get('event_id'), ev.get('event_name') if ev else None, st.get('department') if st else None)
                stats[key] = stats.get(key, 0) + 1
            result = []
            for (eid, ename, dept), count in stats.items():
                result.append({'event_id': eid, 'event_name': ename, 'department': dept, 'count': count})
            return result

        pipeline = [
            {
                '$lookup': {
                    'from': 'students',
                    'localField': 'student_id',
                    'foreignField': '_id',
                    'as': 'student_info'
                }
            },
            {
                '$unwind': '$student_info'
            },
            {
                '$lookup': {
                    'from': 'events',
                    'localField': 'event_id',
                    'foreignField': '_id',
                    'as': 'event_info'
                }
            },
            {
                '$unwind': '$event_info'
            },
            {
                '$group': {
                    '_id': {
                        'event_id': '$event_id',
                        'event_name': '$event_info.event_name',
                        'department': '$student_info.department'
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'_id.event_name': 1, '_id.department': 1}
            }
        ]
        return list(attendance_collection.aggregate(pipeline))

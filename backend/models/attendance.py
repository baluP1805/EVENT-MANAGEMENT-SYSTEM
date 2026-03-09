from datetime import datetime
from supabase_client import get_supabase_client


class Attendance:
    @staticmethod
    def mark_attendance(student_id, event_id, qr_token):
        """Mark attendance for a student in Supabase."""
        sb = get_supabase_client()
        payload = {
            'student_id': student_id,
            'event_id': event_id,
            'qr_token': qr_token,
            'marked_at': datetime.utcnow().isoformat(),
            'status': 'present'
        }
        try:
            res = sb.table('attendance').insert(payload).execute()
            return res.data[0].get('id')
        except Exception as e:
            raise RuntimeError('Failed to insert attendance into Supabase: ' + str(e))

    @staticmethod
    def check_attendance(student_id, event_id):
        """Check if attendance already marked."""
        sb = get_supabase_client()
        res = sb.table('attendance').select('*').match({'student_id': student_id, 'event_id': event_id}).limit(1).execute()
        return res.data[0] if res.data else None

    @staticmethod
    def get_event_attendance(event_id):
        """Get all attendance records for an event."""
        sb = get_supabase_client()
        res = sb.table('attendance').select('*').eq('event_id', event_id).execute()
        return res.data or []

    @staticmethod
    def get_student_attendance(student_id):
        """Get all attendance records for a student."""
        sb = get_supabase_client()
        res = sb.table('attendance').select('*').eq('student_id', student_id).execute()
        return res.data or []

    @staticmethod
    def count_event_attendance(event_id):
        """Count attendance records for an event."""
        sb = get_supabase_client()
        res = sb.table('attendance').select('id').eq('event_id', event_id).execute()
        return len(res.data) if res and res.data else 0

    @staticmethod
    def get_attendance_by_event():
        """Get attendance count grouped by event."""
        sb = get_supabase_client()
        res = sb.table('attendance').select('event_id').execute()
        counts = {}
        for r in (res.data or []):
            eid = r.get('event_id')
            counts[eid] = counts.get(eid, 0) + 1
        return [{'event_id': k, 'count': v} for k, v in counts.items()]

    @staticmethod
    def get_attendance_statistics():
        """Get comprehensive attendance statistics (event + department breakdown)."""
        sb = get_supabase_client()
        att_res = sb.table('attendance').select('*').execute()
        students_res = sb.table('students').select('id, department').execute()
        events_res = sb.table('events').select('id, event_name').execute()
        students = {s['id']: s for s in (students_res.data or [])}
        events = {e['id']: e for e in (events_res.data or [])}
        stats = {}
        for a in (att_res.data or []):
            ev = events.get(a.get('event_id'))
            st = students.get(a.get('student_id'))
            key = (
                a.get('event_id'),
                ev.get('event_name') if ev else None,
                st.get('department') if st else None
            )
            stats[key] = stats.get(key, 0) + 1
        result = []
        for (eid, ename, dept), count in stats.items():
            result.append({'event_id': eid, 'event_name': ename, 'department': dept, 'count': count})
        return result

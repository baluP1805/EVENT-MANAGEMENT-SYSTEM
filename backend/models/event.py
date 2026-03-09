from datetime import datetime
from supabase_client import get_supabase_client


class Event:
    @staticmethod
    def create(event_name, description, date, venue, max_participants=None):
        """Create a new event in Supabase."""
        sb = get_supabase_client()
        payload = {
            'event_name': event_name,
            'description': description,
            'date': date,
            'venue': venue,
            'max_participants': max_participants,
            'total_registered': 0,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        try:
            res = sb.table('events').insert(payload).execute()
            return res.data[0].get('id')
        except Exception as e:
            raise RuntimeError('Failed to insert event into Supabase: ' + str(e))

    @staticmethod
    def find_by_id(event_id):
        """Find event by ID."""
        sb = get_supabase_client()
        res = sb.table('events').select('*').eq('id', event_id).limit(1).execute()
        return res.data[0] if res.data else None

    @staticmethod
    def get_all_events():
        """Get all events ordered by date."""
        sb = get_supabase_client()
        res = sb.table('events').select('*').order('date', desc=False).execute()
        return res.data or []

    @staticmethod
    def update_registration_count(event_id, increment=1):
        """Increment the total_registered count for an event."""
        sb = get_supabase_client()
        ev = Event.find_by_id(event_id)
        if not ev:
            return None
        total = (ev.get('total_registered') or 0) + increment
        return sb.table('events').update({
            'total_registered': total,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', event_id).execute()

    @staticmethod
    def count_events():
        """Count total events."""
        sb = get_supabase_client()
        res = sb.table('events').select('id').execute()
        return len(res.data) if res and res.data else 0

    @staticmethod
    def initialize_default_events():
        """Insert default events if table is empty."""
        defaults = [
            ('Paper Presentation', 'Present your research and technical papers', '2026-03-15', 'Main Auditorium', 100),
            ('Coding Contest', 'Competitive programming challenge', '2026-03-16', 'Computer Lab A', 150),
            ('Gaming Tournament', 'E-sports competition', '2026-03-17', 'Gaming Arena', 80),
            ('Technical Quiz', 'Technology and science quiz competition', '2026-03-18', 'Seminar Hall', 120),
            ('Project Expo', 'Showcase your innovative projects', '2026-03-19', 'Exhibition Hall', 200),
            ('Debugging Challenge', 'Find and fix bugs in code', '2026-03-20', 'Computer Lab B', 100)
        ]
        sb = get_supabase_client()
        res = sb.table('events').select('id').limit(1).execute()
        if res and res.data:
            return False
        inserts = [
            {
                'event_name': name,
                'description': desc,
                'date': date,
                'venue': venue,
                'max_participants': maxp,
                'total_registered': 0,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            for name, desc, date, venue, maxp in defaults
        ]
        try:
            sb.table('events').insert(inserts).execute()
            return True
        except Exception as e:
            print('Error inserting default events:', str(e))
            return False



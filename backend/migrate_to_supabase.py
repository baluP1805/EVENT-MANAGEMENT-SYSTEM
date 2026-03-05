"""
Simple migration helper: copy students and events from MongoDB to Supabase tables.

Run inside the project's virtualenv:

    python migrate_to_supabase.py

Make sure `USE_SUPABASE=true`, `SUPABASE_URL` and `SUPABASE_KEY` are set in your environment.
"""
from pymongo import MongoClient
from config import Config
from supabase_client import get_supabase_client
import base64
from bson import ObjectId
from datetime import datetime


def make_json_serializable(value):
    """Recursively convert Mongo-specific types to JSON-serializable values."""
    if isinstance(value, dict):
        return {k: make_json_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [make_json_serializable(v) for v in value]
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('ascii')
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    # fallback: let json module handle simple types
    return value

# Use a sensible MongoDB fallback when MONGO_URI isn't set in Config
MONGO_URI = Config.MONGO_URI or 'mongodb://localhost:27017'
DATABASE_NAME = Config.DATABASE_NAME or 'college_ems'

# Define allowed columns for each table (fields outside this will be dropped)
ALLOWED_COLUMNS = {
    'students': {'id', 'name', 'email', 'register_number', 'department', 'course', 'year', 'phone_number', 'phone', 'password', 'registered_events', 'created_at', 'updated_at', 'metadata'},
    'events': {'id', 'event_name', 'description', 'location', 'start_time', 'end_time', 'created_by', 'created_at', 'updated_at', 'metadata'},
    'attendance': {'id', 'student_id', 'event_id', 'qr_token', 'marked_at', 'status'},
    'unauthorized_logs': {'id', 'qr_token', 'ip_address', 'user_agent', 'scan_data', 'scanned_at', 'status'}
}

def migrate_collection(collection_name, table_name, transform=None):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    coll = db[collection_name]
    rows = list(coll.find())
    sb = get_supabase_client()
    inserted = 0
    for r in rows:
        # Use MongoDB _id as Supabase id
        mongo_id = r.get('_id')
        r = {k: v for k, v in r.items() if k != '_id'}
        if mongo_id:
            r['id'] = str(mongo_id)
        # Filter to only allowed columns for this table
        allowed = ALLOWED_COLUMNS.get(table_name, set())
        if allowed:
            r = {k: v for k, v in r.items() if k in allowed}
        # Recursively make the row JSON serializable
        r = make_json_serializable(r)
        if transform:
            r = transform(r)
        try:
            res = sb.table(table_name).insert(r).execute()
            # If we got here, insert succeeded (no exception thrown)
            inserted += 1
        except Exception as e:
            # Postgrest APIError will surface here when table doesn't exist or other issues
            msg = str(e)
            if 'Could not find the table' in msg or 'PGRST205' in msg:
                print(f"ERROR: Supabase table '{table_name}' not found. Create the table before running migration.")
                raise
            elif 'duplicate key' in msg or '23505' in msg:
                # Skip duplicate rows and continue
                continue
            else:
                print('Insert error for table', table_name, repr(e))
                raise
    print(f'Inserted {inserted}/{len(rows)} rows into {table_name}')

def migrate_students():
    def transform(s):
        # Supabase expects ISO timestamps for created_at/updated_at
        for k in ('created_at','updated_at'):
            if k in s and hasattr(s[k], 'isoformat'):
                s[k] = s[k].isoformat()
        # Rename phone to phone_number if exists
        if 'phone' in s and 'phone_number' not in s:
            s['phone_number'] = s.pop('phone')
        # Year is stored as text (e.g., "1st Year", "2nd Year") - keep as-is (string not integer)
        return s
    migrate_collection('students', 'students', transform)

def migrate_events():
    def transform(e):
        for k in ('created_at','updated_at'):
            if k in e and hasattr(e[k], 'isoformat'):
                e[k] = e[k].isoformat()
        return e
    migrate_collection('events', 'events', transform)

if __name__ == '__main__':
    if not Config.USE_SUPABASE:
        print('Enable Supabase by setting USE_SUPABASE=true and provide SUPABASE_URL and SUPABASE_KEY')
    else:
        migrate_students()
        migrate_events()

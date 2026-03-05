from models import unauthorized_logs_collection
from datetime import datetime
from config import Config

if Config.USE_SUPABASE:
    from supabase_client import get_supabase_client


class UnauthorizedLog:
    @staticmethod
    def log_unauthorized_scan(qr_token, ip_address=None, user_agent=None, scan_data=None):
        """Log an unauthorized QR scan attempt"""
        payload = {
            'qr_token': qr_token,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'scan_data': scan_data,
            'scanned_at': datetime.utcnow().isoformat(),
            'status': 'unauthorized'
        }
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            try:
                res = sb.table('unauthorized_logs').insert(payload).execute()
                return res.data[0].get('id')
            except Exception as e:
                raise RuntimeError('Failed to insert unauthorized log into Supabase: ' + str(e))

        log_data = {
            'qr_token': qr_token,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'scan_data': scan_data,
            'scanned_at': datetime.utcnow(),
            'status': 'unauthorized'
        }
        result = unauthorized_logs_collection.insert_one(log_data)
        return result.inserted_id

    @staticmethod
    def get_all_logs():
        """Get all unauthorized logs"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('unauthorized_logs').select('*').order('scanned_at', desc=True).execute()
            return res.data or []
        return list(unauthorized_logs_collection.find().sort('scanned_at', -1))

    @staticmethod
    def count_unauthorized():
        """Count total unauthorized scans"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('unauthorized_logs').select('id').execute()
            return len(res.data) if res and res.data else 0
        return unauthorized_logs_collection.count_documents({})

    @staticmethod
    def get_logs_by_date_range(start_date, end_date):
        """Get logs within a date range"""
        if Config.USE_SUPABASE:
            sb = get_supabase_client()
            res = sb.table('unauthorized_logs').select('*').gte('scanned_at', start_date).lte('scanned_at', end_date).order('scanned_at', desc=True).execute()
            return res.data or []

        return list(unauthorized_logs_collection.find({
            'scanned_at': {
                '$gte': start_date,
                '$lte': end_date
            }
        }).sort('scanned_at', -1))

from datetime import datetime
from supabase_client import get_supabase_client


class UnauthorizedLog:
    @staticmethod
    def log_unauthorized_scan(qr_token, ip_address=None, user_agent=None, scan_data=None):
        """Log an unauthorized QR scan attempt."""
        sb = get_supabase_client()
        payload = {
            'qr_token': qr_token,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'scan_data': scan_data,
            'scanned_at': datetime.utcnow().isoformat(),
            'status': 'unauthorized'
        }
        try:
            res = sb.table('unauthorized_logs').insert(payload).execute()
            return res.data[0].get('id')
        except Exception as e:
            raise RuntimeError('Failed to insert unauthorized log: ' + str(e))

    @staticmethod
    def get_all_logs():
        """Get all unauthorized logs ordered by date desc."""
        sb = get_supabase_client()
        res = sb.table('unauthorized_logs').select('*').order('scanned_at', desc=True).execute()
        return res.data or []

    @staticmethod
    def count_unauthorized():
        """Count total unauthorized scans."""
        sb = get_supabase_client()
        res = sb.table('unauthorized_logs').select('id').execute()
        return len(res.data) if res and res.data else 0

    @staticmethod
    def get_logs_by_date_range(start_date, end_date):
        """Get logs within a date range."""
        sb = get_supabase_client()
        res = (
            sb.table('unauthorized_logs')
            .select('*')
            .gte('scanned_at', start_date)
            .lte('scanned_at', end_date)
            .order('scanned_at', desc=True)
            .execute()
        )
        return res.data or []

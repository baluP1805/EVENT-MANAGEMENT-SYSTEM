from supabase import create_client
from config import Config

_client = None

def get_supabase_client():
    global _client
    if _client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise RuntimeError('SUPABASE_URL and SUPABASE_KEY must be set to use Supabase')
        _client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return _client

def reset_supabase_client():
    """Force a fresh client on the next call (used after connection errors)."""
    global _client
    _client = None

def create_user(email, password_hash):
    """Insert a new user into Supabase users table."""
    from app import supabase
    res = supabase.table('users').insert({'email': email, 'password_hash': password_hash}).execute()
    return res.data[0]['id']

def get_user_by_email(email):
    """Fetch a user by email."""
    from app import supabase
    res = supabase.table('users').select('*').eq('email', email).limit(1).execute()
    return res.data[0] if res.data else None

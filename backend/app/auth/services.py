def create_user(email, password_hash):
    """Insert a new user into Supabase users table."""
    from app import supabase
    print(f"DEBUG: Inserting user into Supabase: {email}", flush=True)
    try:
        res = supabase.table('users').insert({'email': email, 'password_hash': password_hash}).execute()
        print("DEBUG: Insert successful", flush=True)
        return res.data[0]['id']
    except Exception as e:
        print(f"DEBUG: Insert failed: {e}", flush=True)
        raise

def get_user_by_email(email):
    """Fetch a user by email."""
    from app import supabase
    print(f"DEBUG: Querying Supabase for email: {email}", flush=True)
    try:
        res = supabase.table('users').select('*').eq('email', email).limit(1).execute()
        print("DEBUG: Query successful", flush=True)
        return res.data[0] if res.data else None
    except Exception as e:
        print(f"DEBUG: Query failed: {e}", flush=True)
        raise

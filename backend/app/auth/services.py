import os
from supabase import create_client

# Build Supabase client ONCE at import time
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG SERVICES SUPABASE_URL =", SUPABASE_URL)
print("DEBUG SERVICES SUPABASE_KEY =", "SET" if SUPABASE_KEY else None)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_KEY is not set. Check your .env and docker-compose.yml")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_user(email, password_hash):
    """Insert a new user into Supabase users table."""
    print(f"DEBUG: Inserting user into Supabase: {email}", flush=True)

    try:
        res = supabase.table("users").insert(
            {"email": email, "password_hash": password_hash}
        ).execute()

        if not res.data or not isinstance(res.data, list):
            raise RuntimeError(f"Supabase insert returned invalid data: {res}")

        user_id = res.data[0].get("id")
        if not user_id:
            raise RuntimeError(f"Supabase insert missing id field: {res.data[0]}")

        print(f"DEBUG: Insert successful, user_id={user_id}", flush=True)
        return user_id

    except Exception as e:
        print(f"DEBUG: Insert failed: {e}", flush=True)
        raise


def get_user_by_email(email):
    """Fetch a user by email."""
    print(f"DEBUG: Querying Supabase for email: {email}", flush=True)

    try:
        res = (
            supabase
            .table("users")
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        if not res.data:
            print("DEBUG: No user found", flush=True)
            return None

        if not isinstance(res.data, list) or not isinstance(res.data[0], dict):
            raise RuntimeError(f"Supabase query returned invalid data: {res.data}")

        print("DEBUG: Query successful", flush=True)
        return res.data[0]

    except Exception as e:
        print(f"DEBUG: Query failed: {e}", flush=True)
        raise

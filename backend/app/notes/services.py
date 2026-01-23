import os
from supabase import create_client

# Build Supabase client ONCE at import time
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG NOTES SERVICES SUPABASE_URL =", SUPABASE_URL)
print("DEBUG NOTES SERVICES SUPABASE_KEY =", "SET" if SUPABASE_KEY else None)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_KEY is not set. Check your .env and docker-compose.yml")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_note(user_id, title, content):
    """Insert a new note for the user."""
    print(f"DEBUG: Inserting note for user_id={user_id}", flush=True)

    try:
        res = supabase.table("notes").insert(
            {"user_id": user_id, "title": title, "content": content}
        ).execute()

        if not res.data or not isinstance(res.data, list):
            raise RuntimeError(f"Supabase insert returned invalid data: {res}")

        note_id = res.data[0].get("id")
        if not note_id:
            raise RuntimeError(f"Supabase insert missing id field: {res.data[0]}")

        print(f"DEBUG: Note inserted successfully, note_id={note_id}", flush=True)
        return note_id

    except Exception as e:
        print(f"DEBUG: Note insert failed: {e}", flush=True)
        raise


def get_notes_for_user(user_id):
    """Fetch all notes for a user."""
    print(f"DEBUG: Fetching notes for user_id={user_id}", flush=True)

    try:
        res = (
            supabase
            .table("notes")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if res.data is None:
            raise RuntimeError(f"Supabase select returned None: {res}")

        if not isinstance(res.data, list):
            raise RuntimeError(f"Supabase select returned invalid data: {res.data}")

        print(f"DEBUG: Fetched {len(res.data)} notes", flush=True)
        return res.data

    except Exception as e:
        print(f"DEBUG: Fetch notes failed: {e}", flush=True)
        raise


def update_note(user_id, note_id, title, content):
    """Update a note if it belongs to the user."""
    print(f"DEBUG: Updating note_id={note_id} for user_id={user_id}", flush=True)

    payload = {}
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content

    if not payload:
        print("DEBUG: No fields to update", flush=True)
        return False

    try:
        res = (
            supabase
            .table("notes")
            .update(payload)
            .eq("id", note_id)
            .eq("user_id", user_id)
            .execute()
        )

        if res.data is None:
            raise RuntimeError(f"Supabase update returned None: {res}")

        if not isinstance(res.data, list):
            raise RuntimeError(f"Supabase update returned invalid data: {res.data}")

        success = len(res.data) > 0
        print(f"DEBUG: Update success={success}", flush=True)
        return success

    except Exception as e:
        print(f"DEBUG: Note update failed: {e}", flush=True)
        raise


def delete_note(user_id, note_id):
    """Delete a note if it belongs to the user."""
    print(f"DEBUG: Deleting note_id={note_id} for user_id={user_id}", flush=True)

    try:
        res = (
            supabase
            .table("notes")
            .delete()
            .eq("id", note_id)
            .eq("user_id", user_id)
            .execute()
        )

        if res.data is None:
            raise RuntimeError(f"Supabase delete returned None: {res}")

        if not isinstance(res.data, list):
            raise RuntimeError(f"Supabase delete returned invalid data: {res.data}")

        success = len(res.data) > 0
        print(f"DEBUG: Delete success={success}", flush=True)
        return success

    except Exception as e:
        print(f"DEBUG: Note delete failed: {e}", flush=True)
        raise

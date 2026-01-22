def create_note(user_id, title, content):
    """Insert a new note for the user."""
    from app import supabase
    res = supabase.table('notes').insert({
        'user_id': user_id, 'title': title, 'content': content
    }).execute()
    return res.data[0]['id']

def get_notes_for_user(user_id):
    """Fetch all notes for a user."""
    from app import supabase
    res = supabase.table('notes').select('*').eq('user_id', user_id).execute()
    return res.data or []

def update_note(user_id, note_id, title, content):
    """Update a note if it belongs to the user."""
    from app import supabase
    res = supabase.table('notes')\
        .update({'title': title, 'content': content})\
        .eq('id', note_id).eq('user_id', user_id)\
        .execute()
    return bool(res.data)

def delete_note(user_id, note_id):
    """Delete a note if it belongs to the user."""
    from app import supabase
    res = supabase.table('notes')\
        .delete()\
        .eq('id', note_id).eq('user_id', user_id)\
        .execute()
    return bool(res.data)

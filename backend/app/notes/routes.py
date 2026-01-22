from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.notes.services import (create_note, get_notes_for_user,
                                update_note, delete_note)

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['POST'])
@jwt_required()
def add_note():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400
    
    try:
        note_id = create_note(user_id, title, content)
        return jsonify({"message": "Note created", "note_id": note_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notes_bp.route('', methods=['GET'])
@jwt_required()
def list_notes():
    user_id = get_jwt_identity()
    notes = get_notes_for_user(user_id)
    return jsonify(notes), 200

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def edit_note(note_id):
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    success = update_note(user_id, note_id, title, content)
    return jsonify({"message": "Note updated"} if success else {"error": "Not found"}), (200 if success else 404)

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def remove_note(note_id):
    user_id = get_jwt_identity()
    success = delete_note(user_id, note_id)
    return jsonify({"message": "Note deleted"} if success else {"error": "Not found"}), (200 if success else 404)

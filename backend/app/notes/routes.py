from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.notes.services import (
    create_note,
    get_notes_for_user,
    update_note,
    delete_note,
)

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["POST"])
@jwt_required()
def add_note():
    user_id = get_jwt_identity()

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400

    try:
        note_id = create_note(user_id, title, content)
        return jsonify({"message": "Note created", "note_id": note_id}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception during note creation: {e}", flush=True)
        return jsonify({"error": "Internal server error"}), 500


@notes_bp.route("/", methods=["GET"])
@jwt_required()
def list_notes():
    user_id = get_jwt_identity()

    try:
        notes = get_notes_for_user(user_id)
        return jsonify(notes), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception during fetching notes: {e}", flush=True)
        return jsonify({"error": "Internal server error"}), 500


@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required()
def edit_note(note_id):
    user_id = get_jwt_identity()

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    title = data.get("title")
    content = data.get("content")

    if not title and not content:
        return jsonify({"error": "At least one of title or content is required"}), 400

    try:
        success = update_note(user_id, note_id, title, content)

        if not success:
            return jsonify({"error": "Note not found"}), 404

        return jsonify({"message": "Note updated"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception during note update: {e}", flush=True)
        return jsonify({"error": "Internal server error"}), 500


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required()
def remove_note(note_id):
    user_id = get_jwt_identity()

    try:
        success = delete_note(user_id, note_id)

        if not success:
            return jsonify({"error": "Note not found"}), 404

        return jsonify({"message": "Note deleted"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception during note deletion: {e}", flush=True)
        return jsonify({"error": "Internal server error"}), 500

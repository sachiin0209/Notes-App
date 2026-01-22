from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.search.service import semantic_search

search_bp = Blueprint('search', __name__)

@search_bp.route('', methods=['POST'])
@jwt_required()
def search_notes():
    user_id = get_jwt_identity()
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    try:
        results = semantic_search(user_id, query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

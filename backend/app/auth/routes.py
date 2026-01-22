from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.auth.services import create_user, get_user_by_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    print("DEBUG: Register endpoint hit", flush=True)
    data = request.json
    email = data.get('email')
    password = data.get('password')
    print(f"DEBUG: Processing registration for {email}", flush=True)
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        print("DEBUG: Checking existing user...", flush=True)
        existing_user = get_user_by_email(email)
        print(f"DEBUG: Existing user check result: {existing_user}", flush=True)
        if existing_user:
            return jsonify({"error": "User already exists"}), 409
        
        password_hash = generate_password_hash(password)
        print("DEBUG: Creating user...", flush=True)
        user_id = create_user(email, password_hash)
        print(f"DEBUG: User created with ID {user_id}", flush=True)
        return jsonify({"message": "User registered", "user_id": user_id}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception during registration: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user = get_user_by_email(email)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = create_access_token(identity=user['id'])
    return jsonify({"access_token": token}), 200

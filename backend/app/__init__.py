from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["*"]}})

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

jwt = JWTManager(app)

# Import blueprints after app is created
from app.auth.routes import auth_bp
from app.notes.routes import notes_bp
from app.search.routes import search_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(notes_bp, url_prefix='/notes')
app.register_blueprint(search_bp, url_prefix='/search')

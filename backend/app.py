import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Debug prints to confirm env wiring (remove later)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG SUPABASE_URL =", SUPABASE_URL)
print("DEBUG SUPABASE_KEY =", "SET" if SUPABASE_KEY else None)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL or SUPABASE_KEY is not set. Check your .env and docker-compose.yml")

# Import Flask app AFTER env is loaded
from app import app  # noqa: E402

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

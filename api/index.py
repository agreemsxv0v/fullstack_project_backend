from flask import Flask
from flask_cors import CORS
import os

# ✅ Simple import - routes is now in the same api folder
from routes.r2_routes import r2_bp

# Load dotenv for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)

# CORS configuration
CORS(app, 
     resources={
         r"/api/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"]
         }
     }
)

# ✅ Only register r2 blueprint
app.register_blueprint(r2_bp, url_prefix="/api/r2")

# Root route
@app.route('/')
@app.route('/api')
def home():
    return "Backend is running successfully 🎉"

# Health check
@app.route('/health')
def health():
    return {"status": "healthy", "message": "Backend is operational"}

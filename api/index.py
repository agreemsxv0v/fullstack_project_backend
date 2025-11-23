from flask import Flask
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.greet_routes import greet_bp
from routes.r2_routes import r2_bp

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

# Register blueprints
app.register_blueprint(greet_bp, url_prefix="/api")
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

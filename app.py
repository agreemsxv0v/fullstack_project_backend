from flask import Flask
from flask_cors import CORS
from routes.greet_routes import greet_bp
from routes.r2_routes import r2_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the app FIRST (before registering blueprints)
app = Flask(__name__)

# ✅ UPDATED CORS: Allow all origins for mobile compatibility
CORS(app, 
     resources={
         r"/api/*": {
             "origins": "*",  # Allow all origins (mobile devices, different IPs, etc.)
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": False
         }
     }
)

# Register routes
app.register_blueprint(greet_bp, url_prefix="/api")
app.register_blueprint(r2_bp, url_prefix="/api/r2")

@app.route('/')
def home():
    return "Backend is running successfully 🎉"

if __name__ == '__main__':
    # ✅ CRITICAL: Use host='0.0.0.0' to accept connections from ANY device on network
    # This allows mobile phones and other devices to connect
    app.run(
        debug=True, 
        host='0.0.0.0',  # Listen on all network interfaces (not just localhost)
        port=int(os.getenv("PORT", 5000))
    )

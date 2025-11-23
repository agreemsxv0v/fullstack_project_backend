from flask import Flask
from flask_cors import CORS
import os

# ✅ Only import r2_routes
# from routes.r2_routes import r2_bp
from api.routes.r2_routes import r2_bp


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

# # for local
# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# import sys

# load_dotenv()

# # Add api folder to path for local testing
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

# from routes.r2_routes import r2_bp

# app = Flask(__name__)

# CORS(app, resources={r"/api/*": {"origins": "*"}})

# app.register_blueprint(r2_bp, url_prefix="/api/r2")

# @app.route('/')
# def home():
#     return "Backend is running locally 🎉"

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask, jsonify
# from flask_cors import CORS

# app = Flask(__name__)

# # Allow requests from your Vite frontend
# CORS(app, origins=["http://localhost:5173"])

# @app.route('/')
# def home():
#     return "Backend is running successfully 🎉"

# @app.route('/api/greet')
# def greet():
#     return jsonify({"message": "Hello from Flask backend!"})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask
from flask_cors import CORS
from routes.greet_routes import greet_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Allow frontend requests
CORS(app, origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")])

# Register blueprints (routes)
app.register_blueprint(greet_bp, url_prefix="/api")

@app.route('/')
def home():
    return "Backend is running successfully 🎉"

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))

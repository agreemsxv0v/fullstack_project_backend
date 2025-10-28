from flask import Blueprint, jsonify

greet_bp = Blueprint("greet", __name__)

@greet_bp.route("/greet")
def greet():
    return jsonify({"message": "Hello from Flask backend!"})

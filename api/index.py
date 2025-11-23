# from flask import Flask
# from flask_cors import CORS
# import os

# # ✅ Simple import - routes is now in the same api folder
# from routes.r2_routes import r2_bp

# # Load dotenv for local development
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except:
#     pass

# app = Flask(__name__)

# # CORS configuration
# CORS(app, 
#      resources={
#          r"/api/*": {
#              "origins": "*",
#              "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#              "allow_headers": ["Content-Type", "Authorization"]
#          }
#      }
# )

# # ✅ Only register r2 blueprint
# app.register_blueprint(r2_bp, url_prefix="/api/r2")

# # Root route
# @app.route('/')
# @app.route('/api')
# def home():
#     return "Backend is running successfully 🎉"

# # Health check
# @app.route('/health')
# def health():
#     return {"status": "healthy", "message": "Backend is operational"}




from flask import Flask, jsonify, redirect
from flask_cors import CORS
import os
import boto3

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

# R2 client configuration
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
)

BUCKET = os.getenv("R2_BUCKET")
PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN")

# Root route
@app.route('/')
@app.route('/api')
def home():
    return "Backend is running successfully 🎉"

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Backend is operational"})

# List all songs
@app.route('/api/r2/songs', methods=["GET"])
def list_songs():
    """List all songs with their public URLs"""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET)

        if "Contents" not in response:
            return jsonify({"songs": []})

        # Return just the filenames (frontend will construct URLs)
        files = [item["Key"] for item in response["Contents"]]

        return jsonify({"songs": files})

    except Exception as e:
        print(f"❌ Error listing songs: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Serve individual song
@app.route('/api/r2/songs/<path:filename>', methods=["GET"])
def serve_song(filename):
    """Redirect to the public R2 URL or generate presigned URL"""
    try:
        # Option 1: Use public domain (if your bucket is publicly accessible)
        if PUBLIC_DOMAIN:
            public_url = f"{PUBLIC_DOMAIN}/{filename}"
            print(f"✅ Redirecting to public URL: {public_url}")
            return redirect(public_url)
        
        # Option 2: Generate presigned URL (if bucket is private)
        else:
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': BUCKET,
                    'Key': filename
                },
                ExpiresIn=3600  # URL valid for 1 hour
            )
            print(f"✅ Redirecting to presigned URL: {presigned_url}")
            return redirect(presigned_url)
            
    except Exception as e:
        print(f"❌ Error serving {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
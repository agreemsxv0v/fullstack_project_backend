# import boto3
# from flask import Blueprint, jsonify
# import os

# r2_bp = Blueprint("r2_bp", __name__)

# # R2 client using your actual .env variable names
# s3 = boto3.client(
#     "s3",
#     endpoint_url=os.getenv("R2_ENDPOINT"),
#     aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
#     aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
# )

# BUCKET = os.getenv("R2_BUCKET")


# @r2_bp.route("/songs", methods=["GET"])
# def list_songs():
#     try:
#         response = s3.list_objects_v2(Bucket=BUCKET)

#         if "Contents" not in response:
#             return jsonify({"songs": []})

#         files = [item["Key"] for item in response["Contents"]]

#         return jsonify({"songs": files})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



import boto3
from flask import Blueprint, jsonify, redirect
import os

r2_bp = Blueprint("r2_bp", __name__)

# R2 client using your actual .env variable names
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
)

BUCKET = os.getenv("R2_BUCKET")
PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN")


@r2_bp.route("/songs", methods=["GET"])
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
        return jsonify({"error": str(e)}), 500


@r2_bp.route("/songs/<path:filename>", methods=["GET"])
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


@r2_bp.route("/songs/<path:filename>", methods=["OPTIONS"])
def serve_song_options(filename):
    """Handle CORS preflight"""
    response = jsonify({"status": "ok"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

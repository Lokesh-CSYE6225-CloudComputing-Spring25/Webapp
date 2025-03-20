# Flask routes for API
import os
from flask import Blueprint, request, make_response, jsonify
from .models import db, HealthCheck, FileMetadata
from datetime import datetime, timezone
import boto3
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime


healthz = Blueprint("healthz", __name__)
bucketz = Blueprint("bucketz", __name__)
# Common headers for all responses
def add_common_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["Content-Length"] = "0"  # Force empty body
    return response

@healthz.route("/healthz", methods=["GET"])
def check_health():

    #Reject query parameters**
    if request.args:  # Check if any query params exist
        response = make_response("", 400)
        return add_common_headers(response)

    # Check if a request body is present
    if request.data:
        response = make_response("", 400)
        return add_common_headers(response)
    try:
        # Simulate inserting a record into the HealthCheck table
        health_entry = HealthCheck()
        db.session.add(health_entry)
        db.session.commit()

        # Success response with no body
        response = make_response("", 200)
        return add_common_headers(response)
    except Exception as e:
        print(f"Error occurred: {e}")
        # Failure response with no body
        response = make_response("", 503)
        return add_common_headers(response)

# Custom error handler for 405
@healthz.errorhandler(405)
def method_not_allowed(error=None):
    response = make_response("", 405)
    return add_common_headers(response)

# Custom error handler for 404
@healthz.errorhandler(404)
def not_found(error=None):
    response = make_response("", 404)
    return add_common_headers(response)

# Custom error handler for 500
@healthz.errorhandler(500)
def internal_server_error(error=None):
    response = make_response("", 500)
    return add_common_headers(response)


# S3 Configuration
s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# POST
@bucketz.route('/v1/file', methods=['POST'])
def upload_file():
    if 'profilePic' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['profilePic']
    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())  # Generate a unique file ID
    user_id = "default-user"  # Placeholder, update as needed (e.g., from request)
    s3_key = f"{BUCKET_NAME}/{user_id}/{file_id}_{filename}"

    # Upload file to S3
    s3.upload_fileobj(file, BUCKET_NAME, s3_key)
    s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

    # Save metadata to database
    new_file = FileMetadata(id=file_id, filename=filename, s3_key=s3_key, s3_url=s3_url, created_at=datetime.utcnow())
    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        "file_name": filename,
        "id": file_id,
        "url": s3_key,
        "upload_date": new_file.created_at.isoformat()
    }), 201


# GET
@bucketz.route('/v1/file/<string:file_id>', methods=['GET'])
def get_file_metadata(file_id):
    file_entry = FileMetadata.query.get(file_id)

    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    return jsonify({
        "file_name": file_entry.filename,
        "id": file_entry.id,
        "url": file_entry.s3_key,
        "upload_date": file_entry.created_at.isoformat()
    }), 200


# DELETE
@bucketz.route('/v1/file/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_entry = FileMetadata.query.get(file_id)

    if not file_entry:
        return jsonify({"error": "File not found"}), 404

    # Delete from S3
    s3.delete_object(Bucket=BUCKET_NAME, Key=file_entry.s3_key)

    # Delete metadata from database
    db.session.delete(file_entry)
    db.session.commit()

    return "", 204  # No Content

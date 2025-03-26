# Flask routes for API
import os
import time
import traceback
from flask import Flask, request, make_response, jsonify
from .models import db, HealthCheck, FileMetadata
from datetime import datetime, timezone
import boto3
from werkzeug.utils import secure_filename
import uuid
from logging import getLogger
from app.metrics import statsd

logger = getLogger("csye6225")

# Initialize Flask App
app = Flask(__name__)

# Common headers for all responses
def add_common_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["Content-Length"] = "0"
    return response

@app.route("/healthz", methods=["GET"])
def check_health():
    start_time = time.time()
    statsd.incr("api.healthz.count")

    if request.args:
        logger.warning("Health check failed: unexpected query parameters")
        return add_common_headers(make_response("", 400))

    if request.data:
        logger.warning("Health check failed: unexpected request body")
        return add_common_headers(make_response("", 400))

    try:
        db_start = time.time()
        health_entry = HealthCheck()
        db.session.add(health_entry)
        db.session.commit()
        statsd.timing("db.healthz.insert", int((time.time() - db_start) * 1000))
        logger.info("Health check passed and recorded to database")
        response = make_response("", 200)
    except Exception:
        logger.error("Health check failed:\n%s", traceback.format_exc())
        response = make_response("", 503)

    statsd.timing("api.healthz.time", int((time.time() - start_time) * 1000))
    return add_common_headers(response)

@app.errorhandler(405)
def method_not_allowed(error=None):
    return add_common_headers(make_response("", 405))

@app.errorhandler(404)
def not_found(error=None):
    return add_common_headers(make_response("", 404))

@app.errorhandler(500)
def internal_server_error(error=None):
    return add_common_headers(make_response("", 500))

s3 = boto3.client('s3')

@app.route('/v1/file', methods=['POST'])
def upload_file():
    api_start = time.time()
    statsd.incr("api.file_upload.count")

    if 'profilePic' not in request.files:
        logger.warning("File upload failed: No file provided")
        return jsonify({"error": "No file provided"}), 400

    try:
        file = request.files['profilePic']
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        user_id = "default-user"
        s3_key = f"{os.getenv('S3_BUCKET_NAME')}/{user_id}/{file_id}_{filename}"

        s3_start = time.time()
        s3.upload_fileobj(file, os.getenv("S3_BUCKET_NAME"), s3_key)
        statsd.timing("s3.file_upload.time", int((time.time() - s3_start) * 1000))

        s3_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.amazonaws.com/{s3_key}"

        db_start = time.time()
        new_file = FileMetadata(id=file_id, filename=filename, s3_key=s3_key, s3_url=s3_url, created_at=datetime.utcnow())
        db.session.add(new_file)
        db.session.commit()
        statsd.timing("db.file_insert.time", int((time.time() - db_start) * 1000))

        logger.info(f"File uploaded: {filename} (ID: {file_id})")
        return jsonify({
            "file_name": filename,
            "id": file_id,
            "url": s3_key,
            "upload_date": new_file.created_at.isoformat()
        }), 201

    except Exception:
        logger.error("File upload failed:\n%s", traceback.format_exc())
        return jsonify({"error": "Upload failed"}), 500

    finally:
        statsd.timing("api.file_upload.time", int((time.time() - api_start) * 1000))

@app.route('/v1/file/<string:file_id>', methods=['GET'])
def get_file_metadata(file_id):
    api_start = time.time()
    statsd.incr("api.file_get.count")

    try:
        db_start = time.time()
        file_entry = FileMetadata.query.get(file_id)
        statsd.timing("db.file_get.time", int((time.time() - db_start) * 1000))

        if not file_entry:
            logger.warning(f"File not found for ID: {file_id}")
            return jsonify({"error": "File not found"}), 404

        logger.info(f"File metadata retrieved for ID: {file_id}")
        return jsonify({
            "file_name": file_entry.filename,
            "id": file_entry.id,
            "url": file_entry.s3_key,
            "upload_date": file_entry.created_at.isoformat()
        }), 200

    except Exception:
        logger.error("Error retrieving file metadata:\n%s", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

    finally:
        statsd.timing("api.file_get.time", int((time.time() - api_start) * 1000))

@app.route('/v1/file/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    api_start = time.time()
    statsd.incr("api.file_delete.count")

    try:
        db_start = time.time()
        file_entry = FileMetadata.query.get(file_id)
        statsd.timing("db.file_lookup.time", int((time.time() - db_start) * 1000))

        if not file_entry:
            logger.warning(f"Delete failed: File not found for ID {file_id}")
            return jsonify({"error": "File not found"}), 404

        s3_start = time.time()
        s3.delete_object(Bucket=os.getenv("S3_BUCKET_NAME"), Key=file_entry.s3_key)
        statsd.timing("s3.file_delete.time", int((time.time() - s3_start) * 1000))

        db_start = time.time()
        db.session.delete(file_entry)
        db.session.commit()
        statsd.timing("db.file_delete.time", int((time.time() - db_start) * 1000))

        logger.info(f"File deleted: {file_id}")
        return "", 204

    except Exception:
        logger.error("File deletion failed:\n%s", traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

    finally:
        statsd.timing("api.file_delete.time", int((time.time() - api_start) * 1000))

# Flask routes for API
from flask import Blueprint, request, make_response
from .models import db, HealthCheck
from datetime import datetime, timezone

healthz = Blueprint("healthz", __name__)

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



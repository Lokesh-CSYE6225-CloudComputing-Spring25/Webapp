# Main entry point for Flask app
from app import create_app

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)


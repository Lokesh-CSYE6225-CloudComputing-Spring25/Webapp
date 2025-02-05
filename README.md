Here’s the full README file expanded in the requested format:

---

# Webapp

## Overview
This is a Flask-based web application with a simple `/healthz` endpoint to perform health checks and interact with a MySQL database. It uses SQLAlchemy for ORM and provides a scalable, modular structure.

---

## Features
- Flask-based application with Blueprints for modular routing.
- `/healthz` endpoint for health checks.
- SQLAlchemy integration for database interactions.
- Secure credential handling using `.env` files.
- Auto-database creation if not present.

---

## Prerequisites
- Python 3.7 or higher
- MySQL database
- Pip for managing Python packages

---

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Webapp
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   Add your database credentials:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

---

## Configuration
The database URL is defined in `app/config.py`. By default:
```python
DB_HOST = "localhost"
DB_NAME = "healthcheck"
```
The app dynamically injects `DB_USER` and `DB_PASSWORD` from the `.env` file.

---

## Running the Application
1. Start the Flask app:
   ```bash
   python run.py
   ```

2. Access the application at:
   ```
   http://127.0.0.1:8080/healthz
   ```

---

## API Endpoints

### **GET /healthz**
- **Description**: Performs a health check by interacting with the database.
- **Response**:
  - `200 OK`: Database is healthy.
  - `503 Service Unavailable`: Database connection failed.
- **Headers**:
  - `Cache-Control`: `no-cache, no-store, must-revalidate`
  - `X-Content-Type-Options`: `nosniff`

---

## Deployment
For deployment:
1. Set the environment variable `FLASK_ENV=production`.
2. Use a production-ready server like `gunicorn`:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 run:app
   ```

---

## Testing
You can test the `/healthz` endpoint with tools like `curl` or Postman:
1. Using `curl`:
   ```bash
   curl -X GET http://127.0.0.1:8080/healthz
   ```

2. Using Postman:
   - Set method to `GET`.
   - Enter the URL: `http://127.0.0.1:8080/healthz`.
   - Send the request and check the response.

---

## Troubleshooting

### Database Connection Issues
- Verify credentials in `.env`.
- Ensure the MySQL service is running and accessible.
- Check the database URL in `config.py`.

### Missing Dependencies
- Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### Debugging
- Enable Flask debug mode during development:
  ```python
  app.run(debug=True)
  ```

---

## Notes
- Ensure `.env` is added to `.gitignore` to secure sensitive credentials.
- Default credentials in `config.py` can be overridden by environment variables.

---
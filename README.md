# Webapp

This repository contains all assignments related to the CSYE 6225 course.

---

## 📌 Table of Contents ()
- [Project Overview](#project-overview)
- [Features](#features)
- [Assignment 1](#assignment-1)
- [Assignment 2](#assignment-2)
- [Prerequisites](#prerequisites)
- [How to Run the Application](#how-to-run-the-application)
- [Deployment on Ubuntu Droplet](#deployment-on-ubuntu-droplet)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## **Project Overview**
This is a Flask-based web application that performs system health checks, interacts with a MySQL database, and supports automated deployment via shell scripts.

---

## **Features**
- Modular Flask application using Blueprints.
- `/healthz` endpoint for health checks.
- SQLAlchemy ORM integration with automatic database setup.
- Secure credential handling using `.env` files.
- Automated deployment using a shell script.
- Systemd configuration for persistent application execution.

---

## **Assignment 1**
### 📝 Overview
This assignment involved setting up a Flask web application with a `/healthz` endpoint, integrating MySQL, and implementing CI/CD.

### 📚 Steps Completed
✅ Flask application setup  
✅ `/healthz` endpoint implemented  
✅ MySQL database setup  
✅ API tests written using `pytest`

---
How to Run the Application
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


## **Assignment 2**
### 📝 Overview
Assignment 2 expands on Assignment 1 by implementing automation with a shell script and deploying to a cloud-based Ubuntu droplet.

### 📚 Steps Completed
✅ Created an automation script (`setup_script.sh`)  
✅ Set up and tested API routes  
✅ Implemented API testing using `pytest`  
✅ Deployed application on DigitalOcean  
✅ Fixed `datetime.utcnow()` deprecation issues  
✅ Configured `systemd` service to keep the app running  
✅ Allowed external access via UFW firewall rules  

---

## **Prerequisites**
- Python 3.7 or higher
- MySQL database
- Pip for managing Python packages
- SSH access to an Ubuntu server (for deployment)

---

## **How to Run the Application**
### 🚀 Steps to Start Locally
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Webapp_Remote
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   Add your database credentials:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```
4. Run the Flask application:
   ```bash
   python run.py
   ```
5. Test the API:
   ```bash
   curl -i http://127.0.0.1:8080/healthz
   ```

---

## **Deployment on Ubuntu Droplet**
1. Connect to the server via SSH:
   ```bash
   ssh -i ~/.ssh/do root@<droplet-ip>
   ```
2. Copy the zipped web application and shell script using SCP:
   ```bash
   scp -i ~/.ssh/do Webapp.zip setup_script.sh root@<droplet-ip>:/root/
   ```
3. Run the shell script to set up the application:
   ```bash
   sudo bash setup_script.sh
   ```
4. Verify that MySQL is running:
   ```bash
   systemctl status mysql
   ```
5. Verify that Python is installed and running:
   ```bash
   python --version
   ```
6. Navigate to the application directory:
   ```bash
   cd /opt/csye6225/
   ```
7. Create a virtual environment and `.env` file (if pulled from GitHub):
   ```bash
   python3 -m venv venv
   touch .env
   ```
8. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
9. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
10. Start the Flask application:
    ```bash
    python run.py
    ```
11. Stop the app and run tests:
    ```bash
    pkill -f run.py  # Stops the running Flask application
    pytest tests/
    ```
12. Allow external access to port 8080:
    ```bash
    sudo ufw allow 8080/tcp
    ```
13. Test the API from your local machine:
    ```bash
    curl -i http://<droplet-ip>:8080/healthz
    ```

---

## **API Endpoints**
### **GET /healthz**
- **Description**: Performs a health check by interacting with the database.
- **Response**:
  - `200 OK`: Database is healthy.
  - `503 Service Unavailable`: Database connection failed.
- **Headers**:
  - `Cache-Control`: `no-cache, no-store, must-revalidate`
  - `X-Content-Type-Options`: `nosniff`

---

## **Testing**
You can test the `/healthz` endpoint using `curl` or Postman:
1. Using `curl`:
   ```bash
   curl -X GET http://127.0.0.1:8080/healthz
   ```
2. Using Postman:
   - Set method to `GET`.
   - Enter the URL: `http://127.0.0.1:8080/healthz`.
   - Send the request and check the response.

---

## **Troubleshooting**
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
Assignment 3

📝 Overview

Assignment 3 focuses on implementing Continuous Integration (CI) with GitHub Actions for the Web App.

📚 Steps Completed

👉 Created and configured GitHub Actions workflow for Web App CI/CD👉 Implemented automated testing using pytest👉 Configured branch protection rules to enforce CI checks before merging PRs👉 Ensured CI runs on every pull request to validate changes

## Web App CI/CD Pipeline
- Runs pytest to validate API functionality.
- Ensures /healthz endpoint behaves correctly.
- Blocks PR merges if any tests fail.
---
## Branch Protection Rules
1. Require status checks before merging
   - Web App CI must pass before merging.
2. Require branches to be up-to-date before merging
   - Ensures branches are synced with the latest code.
   
3. No direct commits to main branch
   - Changes must go through PRs with CI/CD validation.
---
🚀 This setup ensures best practices for Web Application development with Continuous Integration!

---
# WebApp Deployment (Assignment 4)

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [WebApp Setup](#webapp-setup)
- [API Endpoints](#api-endpoints)
- [Systemd Service Management](#systemd-service-management)
- [Testing & Troubleshooting](#testing-troubleshooting)

---

## **Project Overview**
This is a **Flask-based WebApp** that interacts with a MySQL database and includes **automated deployment and health checks**. The application runs as a **systemd service** to ensure high availability and restarts automatically if it crashes.

### ✅ **Key Features:**
- **Modular Flask application** with Blueprints.
- **MySQL database integration** via SQLAlchemy.
- **Secure credential handling** using `.env` files.
- **Automated deployment** with a setup script.
- **Systemd service** for persistent execution.

---

## **Prerequisites**
- Python 3.7 or higher
- MySQL database
- Pip for managing Python packages
- Ubuntu 24.04 server (AWS/GCP instance)

---

## **Installation**
### **Steps to Run Locally**
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd WebApp
   ```
2. Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up `.env` file:
   ```sh
   touch .env
   ```
   Add your database credentials:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```
5. Run the WebApp:
   ```sh
   python run.py
   ```
6. Test the application:
   ```sh
   curl -X GET http://127.0.0.1:8080/healthz
   ```

---

## **WebApp Setup on Server**
### **Automated Deployment Using `setup_webapp.sh`**
This script performs the following actions:
- Installs **MySQL, Python, pip, nginx**.
- Sets up MySQL authentication & creates a database.
- Extracts WebApp files & sets up a virtual environment.
- Moves `.env` securely & installs dependencies.
- Configures **systemd service for WebApp**.

### **Deployment Steps**
1. Copy `setup_webapp.sh` & `Webapp.zip` to the server:
   ```sh
   scp setup_webapp.sh Webapp.zip user@server-ip:/tmp/
   ```
2. SSH into the server:
   ```sh
   ssh user@server-ip
   ```
3. Run the setup script:
   ```sh
   sudo bash /tmp/setup_webapp.sh
   ```
4. Verify systemd service status:
   ```sh
   sudo systemctl status systemd_webapp
   ```

---

## **API Endpoints**
### **GET /healthz**
- **Description**: Performs a health check by interacting with the database.
- **Response**:
  - `200 OK`: Database is healthy.
  - `503 Service Unavailable`: Database connection failed.
- **Headers**:
  - `Cache-Control`: `no-cache, no-store, must-revalidate`
  - `X-Content-Type-Options`: `nosniff`

---

## **Systemd Service Management**
The WebApp runs as a **systemd service**, ensuring automatic startup and crash recovery.

### **Useful Commands:**
- Start the service:
  ```sh
  sudo systemctl start systemd_webapp
  ```
- Restart the service:
  ```sh
  sudo systemctl restart systemd_webapp
  ```
- Check logs:
  ```sh
  journalctl -u systemd_webapp --no-pager | tail -50
  ```

---

## **Testing & Troubleshooting**
### **Health Check API (`/healthz`)**
- Test via `curl`:
  ```sh
  curl -X GET http://<server-ip>:8080/healthz
  ```

### **Troubleshooting Common Issues**
**1. MySQL Connection Issues**
   - Ensure MySQL is running:
     ```sh
     sudo systemctl status mysql
     ```
   - Verify credentials in `.env`.

**2. WebApp Not Running**
   - Restart the systemd service:
     ```sh
     sudo systemctl restart systemd_webapp
     ```
   - Check logs:
     ```sh
     journalctl -u systemd_webapp --no-pager | tail -50
     ```

---

## **🚀 Conclusion**
This WebApp setup ensures a **scalable, production-ready Flask application** with **automated deployment** and **systemd service management**. 🎯


Perfect — thanks for sharing both the Terraform and WebApp README content! You've done an excellent job organizing them.

Here’s what I’ll do next:

1. **Terraform README**  
   ✅ Already looks complete and well-written. No edits needed unless you’d like to update it for Assignment 6-specific logging/metrics changes.

2. **WebApp README**  
   I’ll now create a new **section specifically for Assignment 6** and append it at the end of your current WebApp README (without merging into other sections). This section will document:

   - CloudWatch logging setup
   - Custom metrics tracking (API, DB, S3)
   - IAM + CloudWatch agent configuration
   - Any testing instructions to verify logs and metrics

Give me one moment to prepare that for you.

Here’s the new **Assignment 6** section you can append at the bottom of your existing **WebApp README.md** file:

---

## 📦 Assignment 6 – Logging, Metrics, and CloudWatch Integration

### 📝 Overview

This assignment focuses on:
- CloudWatch Agent setup via Packer
- Logging application events to AWS CloudWatch
- Sending custom metrics for API, database, and S3 usage
- IAM configuration for secure monitoring

---

### ✅ Features Implemented

- ✅ **CloudWatch Agent installed via Packer image**
- ✅ **CloudWatch config copied to `/opt/csye6225/cloudwatch-config.json`**
- ✅ **Custom metrics sent via `statsd`**
- ✅ **Application logs written to `/var/log/csye6225/webapp.log`**
- ✅ **IAM Role with necessary CloudWatch and Logs permissions**
- ✅ **User data script configures and starts agent on boot**

---

### 📄 CloudWatch Agent Configuration

Located at:  
```bash
/opt/csye6225/cloudwatch-config.json
```

Key features:
- Collects logs from `/var/log/csye6225/webapp.log`
- Uses `statsd` for metrics (API count, timing, DB/S3 ops)
- Pushes logs to CloudWatch log group:  
  **`csye6225-webapp-logs`**

---

### 📊 Custom Metrics Tracked

| Metric Name               | Description                                   |
|--------------------------|-----------------------------------------------|
| `api.healthz.count`      | Number of `/healthz` calls                    |
| `api.file_upload.count`  | Number of file uploads                        |
| `api.file_get.count`     | Number of file metadata fetch requests        |
| `api.file_delete.count`  | Number of file deletions                      |
| `api.<endpoint>.time`    | Total request time per endpoint (ms)          |
| `db.<op>.time`           | Time taken for DB operations (ms)             |
| `s3.<op>.time`           | Time taken for S3 upload/delete (ms)          |

StatsD runs on default port `8125`.

---

### 🔐 IAM Role Permissions

Terraform provisions an IAM role attached to EC2:
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`
- `logs:DescribeLogStreams`
- `cloudwatch:PutMetricData`
- `s3:*` (scoped to specific bucket)

---

### 🚀 Deployment Notes

- On EC2 boot, `cloudwatch-config.json` is loaded via:
```bash
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/csye6225/cloudwatch-config.json -s
```

- The `setup_webapp.sh` script automatically configures and starts the agent **only on AWS instances** (detected using instance metadata).

---

### 🔍 Verification Steps

1. **Check Logs**:
   - Navigate to **CloudWatch > Log groups > csye6225-webapp-logs**
   - Look for new log streams per instance

2. **Check Metrics**:
   - Go to **CloudWatch > Metrics > Custom namespaces**
   - Select namespace: `statsd` or `CWAgent`
   - View graphs for API timings, counts, etc.

---

### 🧪 Testing

Use `curl` or Postman to hit various endpoints:
```bash
curl -X GET http://<your-domain>:8080/healthz
curl -X POST http://<your-domain>:8080/v1/file -F "profilePic=@test.jpg"
curl -X GET http://<your-domain>:8080/v1/file/<file_id>
curl -X DELETE http://<your-domain>:8080/v1/file/<file_id>
```

Then validate:
- Logs are updated in CloudWatch
- Metrics show increments & timings under the custom namespace

---



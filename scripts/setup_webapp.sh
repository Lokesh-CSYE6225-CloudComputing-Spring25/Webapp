#!/bin/bash

# Ensure script runs as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)" 
   exit 1
fi

# Load environment variables from .env file
ENV_FILE="/root/.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

# Ensure required variables are set
#if [[ -z "$DB_USER" || -z "$DB_PASS" || -z "$DB_HOST" || -z "$DB_NAME" || -z "$APP_USER" || -z "$APP_GROUP" || -z "$APP_DIR" ]]; then
#    echo "Error: One or more required environment variables are missing in .env file."
#    exit 1
#fi

#echo "Using Database: $DB_NAME on Host: $DB_HOST with User: $DB_USER"
echo "Application Directory: $APP_DIR"
echo "Running as Application User: $APP_USER"

# Function to check if a package is installed
check_package() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 installation failed or is not available. Exiting."
        exit 1
    else
        echo "$1 is installed successfully."
    fi
}

# Update and upgrade system packages
echo "Updating system packages..."
apt update -y && apt upgrade -y

# Install required packages
echo "Installing required packages..."
export DEBIAN_FRONTEND=noninteractive
apt install -y python3 python3-pip python3-venv unzip pkg-config libmysqlclient-dev || { echo "Package installation failed"; exit 1; }

# Check if installations were successful
#check_package "mysql"
check_package "python3"
check_package "pip3"
check_package "unzip"

#Start and enable nginx
#sudo systemctl enable nginx
#sudo systemctl start nginx

# Start and enable MySQL
#systemctl enable mysql && systemctl start mysql

# Change MySQL Root Authentication from auth_socket to mysql_native_password**
#echo "Changing MySQL root authentication method..."
#sudo mysql --user=root <<EOF
#ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$DB_PASS';
#FLUSH PRIVILEGES;
#EOF

# Verify root login with password
#if ! mysql -u root -p"$DB_PASS" -e "SELECT 1;" &> /dev/null; then
#    echo "Error: MySQL root password setup failed."
#    exit 1
#fi
#
#echo "MySQL root password has been successfully set."
#
## Create the database user (Non-root user for security)
#echo "Creating new database user: $DB_USER..."
#sudo mysql -u root -p"$DB_PASS" -e "
#CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';
#GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
#FLUSH PRIVILEGES;" || { echo "Failed to create database user"; exit 1; }
#
## Create the database
#echo "Creating database: $DB_NAME..."
#sudo mysql -u root -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" || { echo "Failed to create database"; exit 1; }

# Create group if it doesn't exist
if ! getent group "$APP_GROUP" >/dev/null; then
    echo "Creating group: $APP_GROUP"
    sudo groupadd --system "$APP_GROUP"
fi

# Create user if it doesn't exist
if ! id "$APP_USER" >/dev/null 2>&1; then
    echo "Creating user: $APP_USER"
    sudo useradd --system --gid "$APP_GROUP" --home "$APP_DIR" -s /usr/sbin/nologin "$APP_USER"
fi

# Setup application directory
echo "Setting up application directory: $APP_DIR..."
sudo mkdir -p "$APP_DIR"
sudo chown -R "$APP_USER":"$APP_GROUP" "$APP_DIR"
sudo chmod -R 750 "$APP_DIR"

# Extract application files
echo "Extracting application files..."
if [ -f "/tmp/Webapp.zip" ]; then
    unzip -o /tmp/Webapp.zip -d "$APP_DIR"
else
    echo "Warning: Application ZIP file not found! Skipping extraction."
fi

# Change to extracted directory
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR" || exit 1
    echo "Changed to application directory: $(pwd)"
else
    echo "Error: Webapp folder not found inside $APP_DIR. Extraction might have failed."
    exit 1
fi


# Setup virtual environment as appuser
echo "Setting up virtual environment..."
sudo -u "$APP_USER" bash -c "cd $APP_DIR && python3 -m venv venv"
sudo chown -R "$APP_USER":"$APP_GROUP" "$APP_DIR/venv"

# Install Python dependencies
if [[ -f "$APP_DIR/requirements.txt" ]]; then
    echo "Installing Python dependencies..."
    sudo -u "$APP_USER" bash -c "cd $APP_DIR && source venv/bin/activate && pip install --no-cache-dir -r requirements.txt" || { echo "Failed to install dependencies"; exit 1; }
else
    echo "Warning: requirements.txt not found in $APP_DIR! Skipping dependency installation."
fi

# Move .env file securely
echo "Moving .env file to the application directory..."
if [[ -f "/root/.env" ]]; then
    sudo mv /root/.env "$APP_DIR/" || { echo "Failed to move .env"; exit 1; }
    
    # Change ownership to appuser
    sudo chown "$APP_USER":"$APP_GROUP" "$APP_DIR/.env"

    # Set secure permissions
    sudo chmod 600 "$APP_DIR/.env"

    echo ".env file moved and secured successfully!"
else
    echo "Warning: .env file not found in /root! Skipping move."
fi

sudo cp /tmp/systemd_webapp.service /etc/systemd/system/systemd_webapp.service

# Create log directory and set permissions
sudo mkdir -p /var/log/csye6225
sudo chown "$APP_USER":"$APP_GROUP" /var/log/csye6225
sudo chmod 750 /var/log/csye6225

sudo systemctl daemon-reload
sudo systemctl enable systemd_webapp
sudo systemctl start systemd_webapp
sudo systemctl restart systemd_webapp

sudo chown -R appuser:appgroup /opt/csye6225/

# --------------------------------------------
# Setup and Start CloudWatch Agent (AWS only)
# --------------------------------------------
if curl --connect-timeout 1 -s http://169.254.169.254/latest/meta-data/instance-id &> /dev/null; then
    echo "Detected AWS environment. Installing CloudWatch Agent..."

    #  Download and install CloudWatch agent manually (official method)
    curl -O https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
    sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
    rm amazon-cloudwatch-agent.deb

    sudo mv /tmp/cloudwatch-config.json /opt/csye6225/cloudwatch-config.json
    sudo chown root:root /opt/csye6225/cloudwatch-config.json
    sudo chmod 644 /opt/csye6225/cloudwatch-config.json

    if [[ -f "/opt/csye6225/cloudwatch-config.json" ]]; then
        echo "Starting CloudWatch Agent using /opt/csye6225/cloudwatch-config.json"
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
            -a fetch-config \
            -m ec2 \
            -c file:/opt/csye6225/cloudwatch-config.json \
            -s
    else
        echo "Warning: CloudWatch config file not found at /opt/csye6225/cloudwatch-config.json. Skipping agent start."
    fi
else
    echo "Skipping CloudWatch Agent setup (Not an AWS environment)"
fi


echo "Setup completed successfully!"
echo "To activate the virtual environment, run: source $APP_DIR/venv/bin/activate"

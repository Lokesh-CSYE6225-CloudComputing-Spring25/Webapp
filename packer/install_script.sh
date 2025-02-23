#!/bin/bash

set -e  # Exit immediately if a command fails

echo "Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

echo "Installing MySQL..."
sudo apt install -y mysql-server python3 python3-pip python3-venv

echo "Creating application directory..."
sudo mkdir -p /opt/csye6225/Webapp
sudo chown -R ubuntu:ubuntu /opt/csye6225/Webapp

echo "Setting up virtual environment..."
cd /opt/csye6225/Webapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Setting up systemd service..."
sudo cp /tmp/systemd_webapp.service /etc/systemd/system/webapp.service
sudo systemctl enable webapp.service

echo "Cleaning up..."
sudo apt autoremove -y

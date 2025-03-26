packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
  }
}

# Define Variables
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "aws_instance_type" {
  type    = string
  default = "t2.micro"
}

variable "gcp_project_id" {
  type    = string
  default = "webappdev-451818"
}

variable "gcp_machine_type" {
  type    = string
  default = "n1-standard-1"
}

variable "gcp_zone" {
  type    = string
  default = "us-central1-c"
}

variable "service_account_email" {
  type    = string
  default = "webappserviceaccount@webappdev-451818.iam.gserviceaccount.com"
}

variable "setup_script_path" {
  type    = string
  default = "scripts/setup_webapp.sh"
}

variable "webapp_zip_path" {
  type    = string
  default = "Webapp.zip"
}

variable "env_file_path" {
  type    = string
  default = ".env"
}

variable "systemd_service_path" {
  type    = string
  default = "systemd_webapp.service"
}

# AWS Source Image
source "amazon-ebs" "ubuntu" {
  ami_name      = "awsWebapp-{{timestamp}}"
  instance_type = var.aws_instance_type
  region        = var.aws_region
  ssh_username  = "ubuntu"
  profile       = "dev"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-noble-24.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["099720109477"] # Canonical's AWS Account ID for Ubuntu
    most_recent = true
  }
}

# GCP Source Image
source "googlecompute" "ubuntu" {
  project_id            = var.gcp_project_id
  image_name            = "gcp-webapp-{{timestamp}}"
  source_image          = "ubuntu-2404-noble-amd64-v20250214"
  source_image_family   = "ubuntu-os-cloud"
  machine_type          = var.gcp_machine_type
  zone                  = var.gcp_zone
  ssh_username          = "ubuntu"
  disk_size             = 25
  service_account_email = var.service_account_email
}

# Build Process
build {
  sources = [
    "source.amazon-ebs.ubuntu",
    "source.googlecompute.ubuntu"
  ]

  # Upload CloudWatch Agent config
  provisioner "file" {
    source      = "cloudwatch-config.json"
    destination = "/opt/csye6225/cloudwatch-config.json"
  }

  # Upload the setup script
  provisioner "file" {
    source      = var.setup_script_path
    destination = "/tmp/setup_webapp.sh"
  }

  # Upload the Webapp.zip file
  provisioner "file" {
    source      = var.webapp_zip_path
    destination = "/tmp/Webapp.zip"
  }

  # Upload the .env file manually for now
  provisioner "file" {
    source      = var.env_file_path
    destination = "/tmp/.env"
  }

  # Upload the systemd file manually for now
  provisioner "file" {
    source      = var.systemd_service_path
    destination = "/tmp/systemd_webapp.service"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/setup_webapp.sh",
      "sudo mv /tmp/.env /root/.env", # Move .env to /root/ for use in script
      "sudo /tmp/setup_webapp.sh"
    ]
  }
}

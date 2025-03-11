packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/invalid/amazon"
    }
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "gcp_project_id" {
  type    = string
  default = "webappdev-451818"
}


# AWS Source Image
source "amazon-ebs" "ubuntu" {
  ami_name      = "awsWebapp-{{timestamp}}"
  instance_type = "t2.micro"
  region        = "us-east-1"
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
  project_id            = "webappdev-451818"
  image_name            = "gcp-webapp-{{timestamp}}"
  source_image          = "ubuntu-2404-noble-amd64-v20250214"
  source_image_family   = "ubuntu-os-cloud"
  machine_type          = "n1-standard-1"
  zone                  = "us-central1-c"
  ssh_username          = "ubuntu"
  disk_size             = 25
  service_account_email = "webappserviceaccount@webappdev-451818.iam.gserviceaccount.com"
}

# Build Process
build {
  sources = [
    "source.amazon-ebs.ubuntu",
    "source.googlecompute.ubuntu"
  ]

  # Upload the setup script
  provisioner "file" {
    source      = "scripts/setup_webapp.sh"
    destination = "/tmp/setup_webapp.sh"
  }

  # Upload the Webapp.zip file
  provisioner "file" {
    source      = "Webapp.zip"
    destination = "/tmp/Webapp.zip"
  }

  # Upload the .env file manually for now
  provisioner "file" {
    source      = ".env"
    destination = "/tmp/.env"
  }

  # Upload the systemd file manually for now
  provisioner "file" {
    source      = "systemd_webapp.service"
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

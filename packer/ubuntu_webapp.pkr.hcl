packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = ">=1.0.0"
    }
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = ">=1.0.0"
    }
  }
}

variable "aws_region" {
  default = "us-east-1"
}

variable "gcp_project_id" {}

variable "gcp_region" {
  default = "us-central1"
}

variable "webapp_repo" {
  default = "/opt/csye6225/Webapp"
}

source "amazon-ebs" "aws_webapp" {
  region      = var.aws_region
  source_ami  = "ami-0fc5d935ebf8bc3bc"  # Ubuntu 24.04 LTS
  instance_type = "t2.micro"
  ssh_username  = "ubuntu"

  ami_name      = "webapp-ubuntu24-${timestamp()}"
  ami_virtualization_type = "hvm"

  tags = {
    Name = "webapp-image"
  }

  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = 10
    volume_type = "gp2"
  }

  provisioner "file" {
    source      = "install_script.sh"
    destination = "/tmp/install_script.sh"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/install_script.sh",
      "sudo /tmp/install_script.sh"
    ]
  }
}

source "googlecompute" "gcp_webapp" {
  project_id     = var.gcp_project_id
  region         = var.gcp_region
  source_image_family = "ubuntu-2404-lts"
  machine_type   = "e2-small"

  image_name     = "webapp-gcp-ubuntu24-${timestamp()}"
  image_family   = "webapp-custom-images"

  disk_size      = 10
  disk_type      = "pd-standard"

  provisioner "file" {
    source      = "install_script.sh"
    destination = "/tmp/install_script.sh"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/install_script.sh",
      "sudo /tmp/install_script.sh"
    ]
  }
}

build {
  sources = ["source.amazon-ebs.aws_webapp", "source.googlecompute.gcp_webapp"]
}

provider "aws" {
  region = var.aws_region
}

resource "random_string" "name" {
  length = 5
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name                    = "mykey"
  associate_public_ip_address = "true"

 provisioner "file" {
    source      = "C:/Users/nkrk1/Documents/GitHub/pythonterraformautomation/Terraform/terraform/jenkinsinstall.sh"
    destination = "/home/ubuntu/jenkinsinstall.sh"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("C:/Users/nkrk1/Desktop/Devops HW/New folder/mykey.pem")
      host        = self.public_ip
    }
  }

  tags = {
    Name = "terrafomr - ${random_string.name.result}"
  }
}

provider "aws" {
  region     = var.aws_region
}


resource "random_string" "name" {
  length = 5
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name                    = "mykey"
  associate_public_ip_address = "true"

  tags = {
    Name = "terrafomr - ${random_string.name.result}"
  }
}

output "instance_public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.example.public_ip
}

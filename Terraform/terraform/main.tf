provider "aws" {
  region = var.aws_region
}

resource "random_string" "name" {
  length = 5
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type

  user_data = file("${path.module}/jenkinsinstall.sh")
  tags = {
    Name = random_string.name.result
  }
}

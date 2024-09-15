provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
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

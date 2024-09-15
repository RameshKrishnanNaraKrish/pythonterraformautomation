variable "aws_region" {
  description = "The AWS region to deploy the infrastructure"
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "The AWS access_key to deploy the infrastructure"
  default     = "us-east-1"
}

variable "aws_secret_key" {
  description = "The AWS secretkeyion to deploy the infrastructure"
  default     = "us-east-1"
}


variable "ami_id" {
  description = "AMI ID for the instance"
  default = "ami-0e86e20dae9224db8"
}

variable "instance_type" {
  description = "Instance type for the instance"
  default     = "t2.micro"
}

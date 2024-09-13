variable "aws_region" {
  description = "The AWS region to deploy the infrastructure"
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for the instance"
}

variable "instance_type" {
  description = "Instance type for the instance"
  default     = "t2.micro"
}

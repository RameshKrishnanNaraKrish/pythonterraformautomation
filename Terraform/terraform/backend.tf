terraform {
  backend "s3" {
    bucket         = "my-tf-test-bucket-backends3"
    key            = "ec2/terraform.tfstate"
    region         = var.aws_region
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}

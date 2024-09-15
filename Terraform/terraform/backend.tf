terraform {
  backend "s3" {
    bucket         = "my-tf-test-bucket-backends3"
    key            = "ec2/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}

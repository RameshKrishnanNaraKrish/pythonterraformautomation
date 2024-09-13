import python_terraform
import logging
import os

# Set up logging
logging.basicConfig(filename='logs/terraform.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Terraform instance
def init_terraform(working_dir):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info('Initializing Terraform')
    return_code, stdout, stderr = tf.init()
    if return_code != 0:
        logging.error(f"Init failed: {stderr}")
    else:
        logging.info(f"Init successful: {stdout}")
    return return_code

# Plan Terraform with dynamic variables
def plan_terraform(working_dir, var_params):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info('Planning Terraform with variables: %s', var_params)
    return_code, stdout, stderr = tf.plan(var=var_params)
    if return_code != 0:
        logging.error(f"Plan failed: {stderr}")
    else:
        logging.info(f"Plan successful: {stdout}")
    return return_code

# Apply Terraform with dynamic variables
def apply_terraform(working_dir, var_params, auto_approve=True):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info('Applying Terraform with variables: %s', var_params)
    return_code, stdout, stderr = tf.apply(var=var_params, skip_plan=True, auto_approve=auto_approve)
    if return_code != 0:
        logging.error(f"Apply failed: {stderr}")
    else:
        logging.info(f"Apply successful: {stdout}")
    return return_code

# Destroy Terraform
def destroy_terraform(working_dir, auto_approve=True):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info('Destroying Terraform')
    return_code, stdout, stderr = tf.destroy(auto_approve=auto_approve)
    if return_code != 0:
        logging.error(f"Destroy failed: {stderr}")
    else:
        logging.info(f"Destroy successful: {stdout}")
    return return_code

if __name__ == '__main__':
    terraform_dir = "terraform/"

    # Define the variables dynamically
    var_params = {
        "aws_region": "us-east-1",
        "ami_id": "ami-0e86e20dae9224db8",
        "instance_type": "t2.micro"
    }

    init_terraform(terraform_dir)
    plan_terraform(terraform_dir, var_params)
    apply_terraform(terraform_dir, var_params)

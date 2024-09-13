import python_terraform
import logging
import argparse

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
    logging.info(f"Planning Terraform with variables: {var_params}")
    return_code, stdout, stderr = tf.plan(var=var_params)
    if return_code != 0:
        logging.error(f"Plan failed: {stderr}")
    else:
        logging.info(f"Plan successful: {stdout}")
    return return_code

# Apply Terraform with dynamic variables
def apply_terraform(working_dir, var_params, auto_approve=True):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info(f"Applying Terraform with variables: {var_params}")
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
    
    # Ensure no '-force' flag is used; only auto_approve=True
    return_code, stdout, stderr = tf.destroy(auto_approve=auto_approve)
    
    if return_code != 0:
        logging.error(f"Destroy failed: {stderr}")  # No decode needed
    else:
        logging.info(f"Destroy successful: {stdout}")  # No decode needed
    
    return return_code

# Execute selected Terraform commands based on Boolean parameters
def execute_selected_commands(init, plan, apply, destroy, working_dir, var_params):
    if init:
        init_terraform(working_dir)
    if plan:
        plan_terraform(working_dir, var_params)
    if apply:
        apply_terraform(working_dir, var_params)
    if destroy:
        destroy_terraform(working_dir)

if __name__ == '__main__':
    # Parse arguments from Jenkins
    parser = argparse.ArgumentParser(description="Terraform Automation with Jenkins")
    parser.add_argument('--tf_init', action='store_true', help='Run terraform init')
    parser.add_argument('--tf_plan', action='store_true', help='Run terraform plan')
    parser.add_argument('--tf_apply', action='store_true', help='Run terraform apply')
    parser.add_argument('--tf_destroy', action='store_true', help='Run terraform destroy')
    parser.add_argument('--aws_region', type=str, required=True, help='AWS region')
    parser.add_argument('--ami_id', type=str, required=True, help='AMI ID')
    parser.add_argument('--instance_type', type=str, required=True, help='EC2 instance type')

    args = parser.parse_args()

    # Working directory for Terraform
    terraform_dir = "terraform/"

    # Define the variables dynamically
    var_params = {
        "aws_region": args.aws_region,
        "ami_id": args.ami_id,
        "instance_type": args.instance_type
    }

    # Execute the selected Terraform commands based on checkboxes
    execute_selected_commands(args.tf_init, args.tf_plan, args.tf_apply, args.tf_destroy, terraform_dir, var_params)

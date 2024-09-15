import python_terraform
import logging
import argparse
import subprocess

# Set up logging
logging.basicConfig(filename='logs/terraform.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Terraform instance
def init_terraform(working_dir):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info('Initializing Terraform')

    return_code, stdout, stderr = tf.init(reconfigure=True)

    if return_code != 0:
        logging.error(f"Init failed: {stderr}")
        print(f"Error: {stderr}")
    else:
        logging.info(f"Init successful: {stdout}")
        print(f"Output: {stdout}")

    return return_code

# Plan Terraform with dynamic variables
def plan_terraform(working_dir, var_params):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info(f"Planning Terraform with variables: {var_params}")

    return_code, stdout, stderr = tf.plan(var=var_params)

    if return_code != 0:
        logging.error(f"Plan failed: {stderr}")
        print(f"Error: {stderr}")
    else:
        logging.info(f"Plan successful: {stdout}")
        print(f"Output: {stdout}")

    return return_code

# Apply Terraform with dynamic variables
def apply_terraform(working_dir, var_params, auto_approve=True):
    tf = python_terraform.Terraform(working_dir=working_dir)
    logging.info(f"Applying Terraform with variables: {var_params}")

    return_code, stdout, stderr = tf.apply(var=var_params, skip_plan=True, auto_approve=auto_approve)

    if return_code != 0:
        logging.error(f"Apply failed: {stderr}")
        print(f"Error: {stderr}")
    else:
        logging.info(f"Apply successful: {stdout}")
        print(f"Output: {stdout}")

    return return_code

# Destroy Terraform
def destroy_terraform(working_dir, auto_approve=True):
    cmd = ["terraform", "destroy"]

    # Add auto-approve flag if necessary
    if auto_approve:
        cmd.append("-auto-approve")

    # Add variable parameters
    for key, value in var_params.items():
        cmd.extend(["-var", f"{key}={value}"])

    # Set working directory and run the command
    try:
        logging.info(f"Running command: {' '.join(cmd)} in {working_dir}")
        result = subprocess.run(cmd, cwd=working_dir, text=True, capture_output=True)
        
        if result.returncode != 0:
            logging.error(f"Destroy failed: {result.stderr}")
            print(f"Error: {result.stderr}")
        else:
            logging.info(f"Destroy successful: {result.stdout}")
            print(f"Output: {result.stdout}")
        
        return result.returncode

    except Exception as e:
        logging.error(f"Error running terraform destroy: {str(e)}")
        print(f"Exception: {str(e)}")
        return 1

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

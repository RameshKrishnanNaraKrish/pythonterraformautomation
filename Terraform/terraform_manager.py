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

def execute_terraform_commands(commands, working_dir, var_params):
    for command in commands:
        if command == 'init':
            init_terraform(working_dir)
        elif command == 'plan':
            plan_terraform(working_dir, var_params)
        elif command == 'apply':
            apply_terraform(working_dir, var_params)
        elif command == 'destroy':
            destroy_terraform(working_dir)
        else:
            logging.error(f"Unknown Terraform command: {command}")

if __name__ == '__main__':
    # Parsing arguments from Jenkins
    parser = argparse.ArgumentParser(description="Terraform Automation")
    parser.add_argument('--actions', type=str, required=True, help='Comma-separated list of Terraform actions: init, plan, apply, destroy')
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

    # Split the actions by comma and execute them in order
    terraform_commands = args.actions.split(',')
    execute_terraform_commands(terraform_commands, terraform_dir, var_params)
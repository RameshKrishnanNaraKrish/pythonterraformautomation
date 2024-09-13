pipeline {
    agent any

    parameters {
        choice(name: 'ACTION', choices: ['init', 'plan', 'apply', 'destroy'], description: 'Choose the Terraform action to perform')
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region')
        string(name: 'AMI_ID', defaultValue: 'ami-0e86e20dae9224db8', description: 'AWS AMI ID')
        string(name: 'INSTANCE_TYPE', defaultValue: 't2.micro', description: 'EC2 Instance Type')
    }

    environment {
        TERRAFORM_DIR = "terraform/"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'bash -c "cd Terraform && python3 -m venv venv && . venv/bin/activate && pip install python-terraform"'
                }
            }
        }

        stage('Execute Terraform Command') {
            steps {
                script {
                    sh """
                    bash -c "cd Terraform && . venv/bin/activate && python3 terraform_manager.py --action ${params.ACTION} --aws_region ${params.AWS_REGION} --ami_id ${params.AMI_ID} --instance_type ${params.INSTANCE_TYPE}"
                    """
                }
            }
        }
    }
}

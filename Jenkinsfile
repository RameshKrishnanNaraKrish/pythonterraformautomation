pipeline {
    agent any

    parameters {
        booleanParam(name: 'TF_INIT', defaultValue: true, description: 'Run terraform init')
        booleanParam(name: 'TF_PLAN', defaultValue: true, description: 'Run terraform plan')
        booleanParam(name: 'TF_APPLY', defaultValue: false, description: 'Run terraform apply')
        booleanParam(name: 'TF_DESTROY', defaultValue: false, description: 'Run terraform destroy')
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
                    sh '''
                    #!/bin/bash
                    cd Terraform
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install python-terraform
                    '''
                }
            }
        }

        stage('Execute Terraform Commands') {
            steps {
                script {
                    sh """
                    #!/bin/bash
                    cd Terraform
                    . venv/bin/activate
                    python3 main.py \
                        --tf_init ${params.TF_INIT} \
                        --tf_plan ${params.TF_PLAN} \
                        --tf_apply ${params.TF_APPLY} \
                        --tf_destroy ${params.TF_DESTROY} \
                        --aws_region ${params.AWS_REGION} \
                        --ami_id ${params.AMI_ID} \
                        --instance_type ${params.INSTANCE_TYPE}
                    """
                }
            }
        }
    }
}
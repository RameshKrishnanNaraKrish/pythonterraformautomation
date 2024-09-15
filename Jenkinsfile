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
        TERRAFORM_DIR = "Terraform/"  // Use consistent directory name (lowercase)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                    cd ${TERRAFORM_DIR}
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install python-terraform
                    '''
                }
            }
        }

        stage('Execute Terraform Commands') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws_credentials',  // Make sure this is the actual ID of your AWS credentials
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        // Build the command dynamically based on the selected parameters
                        def command = "python3 terraform_manager.py"
                        if (params.TF_INIT) {
                            command += " --tf_init"
                        }
                        if (params.TF_PLAN) {
                            command += " --tf_plan"
                        }
                        if (params.TF_APPLY) {
                            command += " --tf_apply"
                        }
                        if (params.TF_DESTROY) {
                            command += " --tf_destroy"
                        }
                        command += " --aws_region ${params.AWS_REGION} --ami_id ${params.AMI_ID} --instance_type ${params.INSTANCE_TYPE}"

                        // Print and run the command
                        echo "Executing command: ${command}"
                        sh """
                            export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                            export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                            cd ${TERRAFORM_DIR}
                            . venv/bin/activate
                            ${command} | tee terraform_output.log
                        """
                    }
                }
            }
        }

         stage('Commit and Push Logs') {
            steps {
                script {
                    sh 'git config --global user.email "jenkins@example.com"'
                    sh 'git config --global user.name "Jenkins"'

                    sh """
                    cd ${TERRAFORM_DIR}

                    git add /logs/terraform.log

                    git commit -m "Update Terraform logs from pipeline execution" || echo "No changes to commit"
                    
                    git push
                    """
                   

                }
            }
         }
    }
}

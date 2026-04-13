pipeline {
    agent any
    
    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_SESSION_TOKEN     = credentials('aws-session-token')
        AWS_DEFAULT_REGION    = 'us-east-1'
        
        AWS_PATH = '/home/salmule/.local/bin/aws'
    }
    
    stages {
        stage('Clonar Repo') {
            steps {
                git branch: 'testing', url: 'https://github.com/SalmuleFish/avanceDeProyectoTest-DevOps.git'
            }
        }
        
        stage('Docker Build Local') {
            steps {
                sh 'echo "Verificando Dockerfile local..."'
                sh 'docker build -t mi-app-stf:latest .'
            }
        }

        stage('Deploy Infra (Terraform)') {
            steps {
                sh 'echo "Aplicando infraestructura con Terraform..."'
                sh '''
                    terraform init
                    terraform apply -auto-approve
                '''
            }
        }

        stage('Reporte de Auditoría (Boto3)') {
            steps {
                script {
                    def accountId = sh(script: "${AWS_PATH} sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                    env.BUCKET_NAME = "reportes-stp-${accountId}"
                }
                sh 'echo "Creando entorno virtual y generando reporte..."'
                sh '''
                    # 1. Creamos el entorno virtual si no existe
                    python3 -m venv venv
                    
                    # 2. Instalamos boto3 dentro del venv
                    ./venv/bin/pip install boto3
                    
                    # 3. Corremos el script usando el python del venv
                    ./venv/bin/python3 automatizacion.py
                '''
            }
        }
    }
    
    post {
        success {
            echo '¡Éxito! Terraform desplegó todo y el reporte de Boto3 se generó correctamente.'
        }
        failure {
            echo 'Fallo en el pipeline. Revisá si falta alguna dependencia o si las credenciales expiraron.'
        }
    }
}
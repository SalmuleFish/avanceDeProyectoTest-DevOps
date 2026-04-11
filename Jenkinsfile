pipeline {
    agent any
    
    environment {
        // Credenciales de AWS Academy
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_SESSION_TOKEN     = credentials('aws-session-token')
        AWS_DEFAULT_REGION    = 'us-east-1'
        
        // Ruta absoluta del ejecutable de AWS en WSL
        AWS_PATH = '/home/salmule/.local/bin/aws'
    }
    
    stages {
        stage('Clonar Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/SalmuleFish/avanceDeProyectoTest-DevOps.git'
            }
        }
        
        stage('Docker Build') {
            steps {
                sh 'echo "Construyendo la imagen de Docker para la app..."'
                // Construye la imagen localmente en WSL
                sh 'docker build -t mi-app-stf:latest .'
            }
        }

        stage('Deploy Infraestructura AWS') {
            steps {
                sh 'echo "Lanzando infraestructura en la nube (CloudFormation)..."'
                // El "|| true" es para que no falle si no hay cambios en el YAML
                sh """
                    ${AWS_PATH} cloudformation deploy \
                    --template-file infraestructura.yaml \
                    --stack-name mi-proyecto-stp \
                    --region ${AWS_DEFAULT_REGION} || true
                """
            }
        }

        stage('Reporte de Recursos (Boto3)') {
            steps {
                script {
                    def accountId = sh(script: "${AWS_PATH} sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                    env.BUCKET_NAME = "reportes-stp-${accountId}"
                }
                sh "./venv/bin/python3 automatizacion.py"
            }
        }
    }
    
    post {
        success {
            echo '¡Éxito! El pipeline se completó, la infraestructura está arriba y el reporte fue generado.'
        }
        failure {
            echo 'Algo falló. Revisá el Console Output para ver si es un tema de credenciales o de sintaxis.'
        }
    }
}
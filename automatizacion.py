import boto3

# Configuración de la sesión (Boto3 usa las credenciales del entorno)
ec2 = boto3.client('ec2', region_name='us-east-1')
s3 = boto3.client('s3')

def generar_reporte():
    print("=== REPORTE DE RECURSOS STF ===")
    
    # 1. Listar Instancias EC2
    print("\n--- Instancias EC2 ---")
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f"ID: {instance['InstanceId']} | Estado: {instance['State']['Name']} | Tipo: {instance['InstanceType']}")

    # 2. Listar Buckets en S3
    print("\n--- Buckets S3 ---")
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        print(f"Nombre del Bucket: {bucket['Name']}")

if __name__ == "__main__":
    generar_reporte()
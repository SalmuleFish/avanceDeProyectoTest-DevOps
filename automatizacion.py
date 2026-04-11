import boto3
import datetime
import os

def generar_y_subir_reporte():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    s3 = boto3.client('s3', region_name='us-east-1')
    
    nombre_bucket = os.getenv('BUCKET_NAME', 'reportes-stp-fallback')
    nombre_archivo = f"reporte-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    
    # Generar el contenido del reporte
    contenido = "=== REPORTE DE RECURSOS STP ===\n\n"
    
    instances = ec2.describe_instances()
    contenido += "--- Instancias EC2 ---\n"
    for reservation in instances['Reservations']:
        for inst in reservation['Instances']:
            contenido += f"ID: {inst['InstanceId']} | Estado: {inst['State']['Name']} | Tipo: {inst['InstanceType']}\n"
    
    # Guardar localmente el reporte
    with open(nombre_archivo, "w") as f:
        f.write(contenido)
    
    # SUBIR AL S3
    print(f"Subiendo {nombre_archivo} al bucket {nombre_bucket}...")
    s3.upload_file(nombre_archivo, nombre_bucket, nombre_archivo)
    print("¡Reporte guardado en S3 con éxito!")

if __name__ == "__main__":
    generar_y_subir_reporte()
provider "aws" {
  region = "us-east-1"
}

# --- RED (VPC, Subnet, IGW) ---
resource "aws_vpc" "vpc_stp" {
  cidr_block           = "10.192.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "STP-Project"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc_stp.id
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.vpc_stp.id
  cidr_block              = "10.192.10.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
  tags = {
    Name = "PublicSubnet1"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc_stp.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# --- SEGURIDAD ---
resource "aws_security_group" "stp_sg" {
  name        = "Permitir SSH y Flask"
  vpc_id      = aws_vpc.vpc_stp.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- COMPUTO ---
resource "aws_instance" "stp_instance" {
  ami           = "ami-0c101f26f147fa7fd"
  instance_type = "t2.micro"
  
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.stp_sg.id]
  iam_instance_profile   = "LabInstanceProfile"
  key_name               = "vockey"

  user_data_replace_on_change = true

  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install docker git -y
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user
              cd /home/ec2-user
              git clone -b testing https://github.com/SalmuleFish/avanceDeProyectoTest-DevOps.git
              cd avanceDeProyectoTest-DevOps
              docker build -t mi-app .
              docker run -d -p 5000:5000 --restart always --name web-stp mi-app
              EOF

  tags = {
    Name = "InstanciaProyectoSTP"
  }
}

# --- ALMACENAMIENTO (S3) ---
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "stp_bucket" {
  bucket = "reportes-stp-${data.aws_caller_identity.current.account_id}"
  force_destroy = true 
}

# --- MONITOREO (CloudWatch) ---
resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "STP-High-CPU-Alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "70"

  dimensions = {
    InstanceId = aws_instance.stp_instance.id
  }
}
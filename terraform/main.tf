locals {
  ssh_cidr = var.my_ip == "0.0.0.0" ? "0.0.0.0/0" : "${var.my_ip}/32"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# AWS Academy Learner Lab resets the default VPC's main route table (dropping the
# internet route) between sessions; managing it here restores it on every apply.
resource "aws_default_route_table" "default" {
  default_route_table_id = data.aws_vpc.default.main_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = data.aws_internet_gateway.default.id
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.ssh_cidr]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                         = "ami-0e86e20dae9224db8" # Ubuntu 22.04 LTS (us-east-1)
  instance_type               = var.instance_type
  key_name                    = var.key_name
  security_groups             = [aws_security_group.web_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "academy-web"
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_instance" "web-1" {
  count = local.count[terraform.workspace]
  ami = data.aws_ami.ubuntu.id
  instance_type = local.instance_type[terraform.workspace]

  tags = {
    Name = "terraform-${count.index + 1}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_instance" "web-2" {
  for_each = local.instance_count[terraform.workspace]
  ami = data.aws_ami.ubuntu.id
  instance_type = each.value

  tags = {
    Name = "terraform-${each.key}"
  }
}
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}

output "region" {
  value = data.aws_region.current.name
}

output "subnet_id" {
  description = "The id of subnet assigned to the instances."
  value = aws_subnet.main.id
}

output "web-1_private_ips" {
  description = "The private IP address assigned to the web-1 instances."
  value = {
    for instance in aws_instance.web-1:
      instance.id => instance.private_ip
  }
}

output "web-2_private_ips" {
  description = "The private IP address assigned to the web-2 instances."
  value = {
    for instance in aws_instance.web-2:
      instance.id => instance.private_ip
  }
}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "caller_user" {
  value = data.aws_caller_identity.current.user_id
}

output "region" {
  value = data.aws_region.current.name
}

output "private_ip" {
  description = "The private IP address assigned to the instance."
  value = aws_instance.web.private_ip
}

output "subnet_id" {
  description = "The id of subnet assigned to the instance."
  value = aws_subnet.main.id
}
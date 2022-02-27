terraform {
  backend "s3" {
    bucket = "sahaviev-terraform-states"
    key    = "terraform-state"
    region = "us-east-1"
  }
}
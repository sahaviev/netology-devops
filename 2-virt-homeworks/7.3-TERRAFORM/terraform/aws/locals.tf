
locals {
  instance_type = {
    stage = "t2.micro"
    prod = "t3.micro"
  }
  count = {
    stage = 1
    prod = 2
  }
  instance_count = {
    stage = {
      "vm1" = "t2.micro"
    }
    prod = {
      "vm1" = "t3.micro"
      "vm2" = "t3.micro"
    }
  }
}

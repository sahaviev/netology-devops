provider "yandex" {
  service_account_key_file = "key.json"
}

resource "yandex_compute_instance" "node01" {
  name = "terraform-example"

  resources {
    cores  = 4
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = "fd83n3uou8m03iq9gavu"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.default.id
    nat = true
  }

  metadata = {
    ssh-keys = "centos:${file("~/.ssh/id_rsa.pub")}"
  }
}

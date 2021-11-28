#!/usr/bin/env python3

import socket
import yaml
import json


def save_service_to_txt(filename, _services):
    with open(filename, 'w') as f:
        for hostname in _services:
            f.write(f'{hostname} - {_services[hostname]}\n')


def save_to_yaml(filename, data):
    with open(filename, 'w') as f:
        f.write(yaml.dump(data, indent=4, explicit_start=True))


def save_to_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=4))


def load_services_from_txt(filename):
    _services = {}
    with open(filename, 'r') as f:
        for data in f:
            check = data.split(' - ')
            _services[check[0]] = check[1].strip()
    return _services


def check_services(_services):
    for hostname in _services:
        current_ip = socket.gethostbyname(hostname)
        if current_ip != _services[hostname]:
            print(f'[ERROR] {hostname} IP mismatch: {_services[hostname]} {current_ip}')
            _services[hostname] = current_ip
        else:
            print(f'{hostname} - {current_ip}')
    return _services


services = check_services(load_services_from_txt('services-list.txt'))

save_service_to_txt('services-list.txt', services)
save_to_yaml('services-list.yml', services)
save_to_json('services-list.json', services)

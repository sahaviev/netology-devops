#!/usr/bin/env python3

import socket

services = {}

with open('services-list.txt', 'r') as f:
    for data in f:
        check = data.split(' - ')
        services[check[0]] = check[1].strip()

for hostname in services:
    current_ip = socket.gethostbyname(hostname)
    if current_ip != services[hostname]:
        print(f'[ERROR] {hostname} IP mismatch: {services[hostname]} {current_ip}')
        services[hostname] = current_ip
    else:
        print(f'{hostname} - {current_ip}')


with open('services-list.txt', 'w') as f:
    for hostname in services:
        f.write(f'{hostname} - {services[hostname]}\n')
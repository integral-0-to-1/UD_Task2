import re
import csv
import json
import argparse

def parse_log_file(path):
    ipv4 = r'\d*[.]\d*[.]\d*[.]\d*'
    ipv6 = r"\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b"
    domain = r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b"
    is_binding = r"ISBindingImageDescriptor."

    ip_addresses = []
    ipv6_addresses = []
    domains = []
    is_binding_image_descriptors = []

    with open(path, 'r') as file:
        for line in file:
            ips = re.findall(ipv4, line)
            ip_addresses.extend(ips)

            ipv6s = re.findall(ipv6, line)
            ipv6_addresses.extend(ipv6s)

            domains_found = re.findall(domain, line)
            domains.extend(domains_found)

            is_binding_images = re.findall(is_binding, line)
            is_binding_image_descriptors.extend(is_binding_images)

    return ip_addresses, ipv6_addresses, domains, is_binding_image_descriptors

# Отримання аргументів з командного рядка
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--json", action="store_true")
parser.add_argument("--csv", action="store_true")
parser.add_argument("--console", action="store_true")
args = parser.parse_args()

log_path = "Task_2_2.log"
ip_addresses, ipv6_addresses, domains, is_binding_image_descriptors = parse_log_file(log_path)

if args.json:
    json_data = {
        "IPv4 Addresses": ip_addresses,
        "IPv6 Addresses": ipv6_addresses,
        "Domains": domains,
        "ISBindingImageDescriptor": is_binding_image_descriptors
    }
    with open("results2.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("Результати збережено у файлі 'results2.json'")

if args.csv:
    with open("results2.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["IPv4 Addresses", "IPv6 Addresses", "Domains", "ISBindingImageDescriptor"])
        writer.writerows(zip(ip_addresses, ipv6_addresses, domains, is_binding_image_descriptors))
    print("Результати збережено у файлі 'results.csv'")

if args.console:
    print("IPv4 Addresses:")
    print(ip_addresses)
    print("IPv6 Addresses:")
    print(ipv6_addresses)
    print("Domains:")
    print(domains)
    print("ISBindingImageDescriptor:")
    print(is_binding_image_descriptors)
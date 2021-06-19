#!/usr/bin/env python

import os
import requests
import time
import logging
import subprocess

import CloudFlare

zone_filters = [element.strip() for element in os.environ.get('ZONES', '').split(sep=',')]
delay = int(os.environ.get('DELAY', '300'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger('ddns')


def filter_zones(zone_filters, zones):
    return [zone for zone in zones if zone['name'] in zone_filters]


def is_A_record(record):
    return record['type'] == 'A'


def filler_A_root_records(cf, zone):
    zone_id, zone_name = zone['id'], zone['name']

    records = cf.zones.dns_records.get(zone_id)
    return [record for record in records
            if is_A_record(record) and record['name'] == zone_name]


def filter_keys(d, l):
    return {k: d[k] for k in l if k in d}


def clear_dead_records(cf, zone):
    dns_records = filler_A_root_records(cf, zone)

    zone_id = zone['id']
    for record in dns_records:
        ip = record['content']
        if subprocess.run(['ping', '-W', '1', '-c', '1', ip], capture_output=True).returncode != 0:
            record_id = record['id']
            cf.zones.dns_records.delete(zone_id, record_id)
            pretty_record = filter_keys(record, ['content', 'name', 'type'])
            logger.info(f"Deleted stale {pretty_record} record.")


def record_exists(new_record, dns_records):
    return any(record['name'] == new_record['name'] and record['content'] == new_record['content'] for record in dns_records)


def add_record(cf, zone, ip):
    existing_records = filler_A_root_records(cf, zone)

    zone_id, zone_name = zone['id'], zone['name']
    new_record = {'name': zone_name, 'type': 'A', 'content': ip}

    if not record_exists(new_record, existing_records):
        cf.zones.dns_records.post(zone_id, data=new_record)
        logger.info(f"Added {new_record} record in zone {zone_name}.")
    else:
        logger.info(f"Record {new_record} already exists in zone {zone_name}.")


def main():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()

    cf = CloudFlare.CloudFlare()
    zones = filter_zones(zone_filters, cf.zones.get())

    if len(zones) == 0:
        logger.warning("No zones found.")

    for zone in zones:
        clear_dead_records(cf, zone)
        add_record(cf, zone, ip)


if __name__ == '__main__':
    while True:
        try:
            main()
        except e:
            logger.error(e)
        time.sleep(delay)

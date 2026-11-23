#!/usr/bin/env python3
"""Kepware IoT Platform REST API Controller.

Usage:
    python kepware-iot.py --base https://localhost:51234 list-resources
    python kepware-iot.py --base https://localhost:51234 read-tag Channel Device Tag
    python kepware-iot.py --base https://localhost:51234 write-tag Channel Device Tag 123
    python kepware-iot.py --base https://localhost:51234 --token "eyJ..." read-tag Channel Device Tag
"""

import argparse
import requests
import json
import sys


def get_base_url(base, insecure=False):
    url = base.rstrip('/')
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    if insecure:
        requests.packages.urllib3.disable_warnings()
    return url


def list_resources(base_url, token=None, insecure=False):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.get(
            f'{base_url}/api/v1/resources',
            headers=headers,
            verify=not insecure,
            timeout=10
        )
        resp.raise_for_status()
        resources = resp.json()
        print(f'RESOURCES| Count: {len(resources)}')
        for r in resources:
            print(f'RESOURCE| {r.get("name", "")} | {r.get("type", "")} | {r.get("status", "")}')
    except Exception as e:
        print(f'ERROR| {str(e)}')


def read_tag(base_url, channel, device, tag, token=None, insecure=False):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.get(
            f'{base_url}/api/v1/resources/{channel}/{device}/{tag}/value',
            headers=headers,
            verify=not insecure,
            timeout=10
        )
        resp.raise_for_status()
        value = resp.json()
        print(f'VALUE| {channel}/{device}/{tag} | {json.dumps(value)}')
    except requests.exceptions.HTTPError as e:
        print(f'ERROR| HTTP {e.response.status_code}: {e.response.text}')
    except Exception as e:
        print(f'ERROR| {str(e)}')


def write_tag(base_url, channel, device, tag, value, token=None, insecure=False):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.put(
            f'{base_url}/api/v1/resources/{channel}/{device}/{tag}/value',
            headers=headers,
            json=value,
            verify=not insecure,
            timeout=10
        )
        resp.raise_for_status()
        print(f'OK| Wrote {value} to {channel}/{device}/{tag}')
    except requests.exceptions.HTTPError as e:
        print(f'ERROR| HTTP {e.response.status_code}: {e.response.text}')
    except Exception as e:
        print(f'ERROR| {str(e)}')


def device_status(base_url, channel, device, token=None, insecure=False):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        resp = requests.get(
            f'{base_url}/api/v1/resources/{channel}/{device}/status',
            headers=headers,
            verify=not insecure,
            timeout=10
        )
        resp.raise_for_status()
        status = resp.json()
        print(f'STATUS| {channel}/{device} | {json.dumps(status)}')
    except Exception as e:
        print(f'ERROR| {str(e)}')


def main():
    parser = argparse.ArgumentParser(description='Kepware IoT Platform Controller')
    parser.add_argument('--base', required=True, help='Base URL (e.g., https://localhost:51234)')
    parser.add_argument('--token', help='Bearer token for auth')
    parser.add_argument('--insecure', action='store_true', help='Skip TLS verification')

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')
    subparsers.add_parser('list-resources')

    rp = subparsers.add_parser('read-tag')
    rp.add_argument('channel')
    rp.add_argument('device')
    rp.add_argument('tag')

    wp = subparsers.add_parser('write-tag')
    wp.add_argument('channel')
    wp.add_argument('device')
    wp.add_argument('tag')
    wp.add_argument('value', help='JSON value to write')

    sp = subparsers.add_parser('device-status')
    sp.add_argument('channel')
    sp.add_argument('device')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    base_url = get_base_url(args.base, args.insecure)

    if args.action == 'list-resources':
        list_resources(base_url, args.token, args.insecure)
    elif args.action == 'read-tag':
        read_tag(base_url, args.channel, args.device, args.tag, args.token, args.insecure)
    elif args.action == 'write-tag':
        write_tag(base_url, args.channel, args.device, args.tag, args.value, args.token, args.insecure)
    elif args.action == 'device-status':
        device_status(base_url, args.channel, args.device, args.token, args.insecure)


if __name__ == '__main__':
    main()

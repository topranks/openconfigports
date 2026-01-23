#!/usr/bin/python3

import argparse
from pathlib import Path
from getpass import getpass
import requests
import sys
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description='OpenConfig Serial Port Config Generator')
parser.add_argument('-s', '--scs', help='Name of Openconfig serial console server (i.e. "scs-c1-eqiad")', type=str, required=True)
parser.add_argument('-n', '--netbox', help='Netbox server IP / Hostname', type=str, default="netbox.wikimedia.org")
parser.add_argument('-k', '--key', help='Netbox API Token / Key', type=str, default='')
args=parser.parse_args()

USER_AGENT = "Openconfig serial port setup script"

def main():
    """ Read GraphQL query from disk, execute, then render Jinja2 template with results"""
    gql_query = Path('console_server.gql').read_text()
    gql_vars = {'device': args.scs}
    nb_data = get_graphql_query(gql_query, gql_vars, USER_AGENT)

    if len(nb_data['device_list']) == 0:
        print(f"ERROR: Could not find device {args.scs}.")
        sys.exit(1)

    # Generate config using Jinja2 template
    file_loader = FileSystemLoader(searchpath="./")
    env = Environment(loader=file_loader)
    template = env.get_template('opengear_ports.j2')
    output = template.render(ports = nb_data['device_list'][0]['consoleserverports'], scs = args.scs)
    filename = f"{args.scs}.conf"
    with open(filename, 'w') as f:
        f.write(output)
    print(f"Wrote config to {filename}")


def get_graphql_query(query: str, variables: dict = None, agent: str = "test script") -> dict:
    """Sends graphql query to netbox and returns JSON result as dict"""
    url = f"https://{args.netbox}/graphql/"

    nb_key = args.key if args.key else getpass(prompt="Netbox API token: ")

    headers = {
        'Authorization': f'Token {nb_key}',
        'User-Agent': agent,
        'Content-Type': "application/json"
    }

    data = {"query": query}
    if variables is not None:
        data['variables'] = variables

    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['data']


if __name__=="__main__":
    main()

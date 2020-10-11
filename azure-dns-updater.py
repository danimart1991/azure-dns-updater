from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.dns import DnsManagementClient
from requests import get
from socket import gethostbyname
import time
import logging
import os
import sys

def definevar(var: str, cast: type) -> str:
    if var in os.environ:
        return os.environ[var]
    else:
        args = sys.argv[1:]
        for arg in args:
            arg_clean = arg.replace('--','',1).split('=')
            if arg_clean[0] == var:
                return cast(arg_clean[1])
    return   

TENANT_ID = definevar('TENANT_ID', str)
APP_ID = definevar('APP_ID', str)
APP_SECRET = definevar('APP_SECRET', str)
SUBSCRIPTION_ID = definevar('SUBSCRIPTION_ID', str)
RESOURCE_GROUP = definevar('RESOURCE_GROUP', str)
RECORD_SET = definevar('RECORD_SET', str)
DOMAIN = definevar('DOMAIN', str)
interval = definevar('INTERVAL', int)
INTERVAL = 300 if interval is None else interval

ip = get('https://api.ipify.org').text

credentials = ServicePrincipalCredentials(
    client_id = APP_ID,
    secret = APP_SECRET,
    tenant = TENANT_ID
)

dns_client = DnsManagementClient(
    credentials,
    SUBSCRIPTION_ID
)

while True:
    try:
        print(f'[{time.strftime("%H:%M:%S")}]')
        print(f'Checking {RECORD_SET} record set...')
        public_ip = ip
        print(f'Public IP address: {public_ip}')
        host = ("a." if RECORD_SET == "*" else ("" if RECORD_SET == "@" else RECORD_SET + ".")) + DOMAIN
        current_ip = gethostbyname(host) 
        print(f'Current IP address: {current_ip}')

        if public_ip == current_ip:
            print("No change")
        else:
            record_set = dns_client.record_sets.create_or_update(
                RESOURCE_GROUP,
                DOMAIN,
                RECORD_SET,
                'A',
                {
                    "ttl": INTERVAL,
                    "arecords": [
                        {
                            "ipv4_address": public_ip
                        }
                    ]
                }
            )
            print("Record changed")
    except Exception as c:
        logging.error(c)
    
    time.sleep(INTERVAL)
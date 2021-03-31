import config
from suds.client import Client
from sys import argv


# billing connection
endpoint = config.wsdl_url
service_url = config.service_url
client = Client(endpoint, faults=False)
client.set_options(location=service_url)
manager = client.service.Login(config.billing_login, config.billing_password)

# OLT ip
device_ip = argv[1]

# information from billing
device = client.service.getDevices(flt={'ip': device_ip})
ports = client.service.getPorts(flt={'deviceid': device[1][0]['deviceid']})
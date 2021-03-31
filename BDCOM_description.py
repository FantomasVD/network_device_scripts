import config
import telnetlib
from suds.client import Client
from sys import argv


# for OLT configuration
def config_device(device_ip, password, login, ports):
    tn = telnetlib.Telnet(device_ip)
    tn.read_until(b"Username: ")
    tn.write(login.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b'config\n')
    for port in ports[1]:
        if len(str(port['name'])) > 2:
            interface = 'Epon0/'+str(port['name'])[0]+':'+str(port['name'])[1:]
            login_id = port['login']
            config_port = f'interface {interface}\n'
            config_port = config_port.encode('ASCII')
            tn.write(config_port)
            description_port = f'description {login_id}\n'
            description_port = description_port.encode('ASCII')
            tn.write(description_port)
    tn.write(b'exit\n')
    tn.write(b'exit\n')
    tn.write(b'write all\n')
    tn.write(b'exit\n')
    tn.write(b'exit\n')
    tn.read_all().decode('ascii')
    print('Done')


# OLT ip
device_ip = argv[1]

if __name__ == '__main__':

    # billing connection
    endpoint = config.wsdl_url
    service_url = config.service_url
    client = Client(endpoint, faults=False)
    client.set_options(location=service_url)
    manager = client.service.Login(config.billing_login, config.billing_password)


    # information from billing
    device = client.service.getDevices(flt={'ip': device_ip})
    ports = client.service.getPorts(flt={'deviceid': device[1][0]['deviceid']})


    # OLT configuration
    config_device(device_ip, config.device_password, config.device_login, ports)

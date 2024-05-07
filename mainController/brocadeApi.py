from netmiko import ConnectHandler, NetmikoTimeoutException
import re

class Brocade:

    status = None

    def __init__(self, ipAddress, userName, passWord):
        try:
            brocade_router = {
                'device_type': 'ruckus_fastiron',
                'host': ipAddress,
                'username': userName,
                'password': passWord,
                #'secret': 'enablepass',
                'port': 22,
                # "session_log": "netmiko_session.log"
            }

            ssh = ConnectHandler(**brocade_router)
            self.status = 1
            self.ssh = ssh
            ssh.enable()
            # result = ssh.send_command('sh mac-address vlan 100 | exclude 1/1/48')
            # result = ssh.send_command('show lldp neighbors')
            print("enviando comando")
            # result = ssh.send_command('sh mac-address vlan 100')
            # result = ssh.send_command('show interfaces brief')
            # print(result)
        except NetmikoTimeoutException:
            print("Connection failed")
    
    def getDeviceName(self):
        deviceName = self.ssh.find_prompt()[:-1]
        return deviceName
    
    def parse(self, string, wlan="", vlan="", stations=""):
        lista = {}
        for line in re.split(r"[~\r\n]+", string):
            if ':' not in line:
                print(line)
                continue			
            key_value = re.split(":", line)
            #value = line.split(':', maxsplit=1)[1].strip()
            lista = {key_value[0].strip():key_value[1].strip()}
            print(lista)
            # if line.startswith('SSID'):
        return lista

    def getData(self):
        raw_data = self.ssh.send_command('show version')
        deviceData = self.parse(raw_data)
        raw_mac_address = self.ssh.send_command('show chassis')
        mac_address = self.parse(raw_mac_address)
        print(mac_address['Management MAC'])
        data = {
            'mac address':mac_address['Management MAC'],
            'serial':deviceData['Serial  #'],
            'model':deviceData['HW'],
            'version':deviceData['SW'],
            }        
        return data    
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import re
import socket

class Brocade:

    status = None

    def __init__(self, ipAddress, userName, passWord, enablePassword=None):
        self.password = passWord
        if not enablePassword:
            enablePassword = passWord
        try:
            brocade_router = {
                'device_type': 'ruckus_fastiron',
                'host': ipAddress,
                'username': userName,
                'password': passWord,
                'secret': enablePassword,
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
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f"Error de Netmiko: {e}")
            self.status = 0

        except socket.error as e:
            print(f"Error de socket: {e}")
            self.status = 0

        except Exception as e:
            print(f"Otro error: {e}")
            self.status = 0 
    
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
            lista.update({key_value[0].strip():key_value[1].strip()})
            # print(lista)
            # if line.startswith('SSID'):
        return lista

    def parse_mac(self, string):
        mac_address = string.replace(".", "")
        formatted_mac_address = ':'.join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
        return formatted_mac_address

    def parse_ifcs(self, string):
        pattern = r'^(\d+/\d+/\d+)\s+(\S+)\s+'
        matches = re.findall(pattern, string, re.MULTILINE)
        result = {}
        for match in matches:
            mac = self.parse_mac(match[1])
            result[match[0]] = mac

        # Imprimir el diccionario resultante
        return result

    def get_clients(self):
        result = self.ssh.send_command('show lldp neighbors')
        print(result)
        interfaces = self.parse_ifcs( result)
        return interfaces
    
    def getInterfacesDevices(self):
        result = self.ssh.send_command('show lldp neighbors')
        print(result)
        interfaces = self.parse_ifcs( result)
        return interfaces

    def getData(self):
        raw_data = self.ssh.send_command('show version')
        deviceData = self.parse(raw_data)
        raw_mac_address = self.ssh.send_command('show chassis')
        mac_address = self.parse(raw_mac_address)
        mac = self.parse_mac(mac_address['Management MAC'])
        # print(deviceData)
        data = {
            'mac address':mac,
            'serial':deviceData['Serial  #'],
            'model':deviceData['HW'],
            'version':deviceData['SW'],
            }        
        return data
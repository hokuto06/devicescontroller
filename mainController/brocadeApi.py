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
        if string:
            lines = re.split(r"[~\r\n]+", string)
            lista = {"wlan": wlan, "stations": stations, "vlan": vlan}
            linesCount = 0
            for line in lines:
                if re.search(':', line):
                    linesCount = linesCount+1
                    _list = re.split(":", line, 1)
                    key = _list[0].lstrip().strip()
                    value = _list[1].lstrip().strip()
                    lista[key] = value
            if linesCount == 1:
                lista = value
            return lista



    def getData(self):
        raw_version_data = self.ssh.sendCommand('show version')
        deviceData = self.parse(raw_version_data.decode("utf-8"))
        raw_mac_address = self.ssh.sendCommand('show chasis')
        mac_address = self.parse(raw_mac_address.decode("utf-8"))
        data = {
            'mac address':mac_address['Management MAC'],
            'serial':deviceData['Serial  #'],
            'model':deviceData['UNIT 1'],
            'version':deviceData['SW'],
            }        
        return data    
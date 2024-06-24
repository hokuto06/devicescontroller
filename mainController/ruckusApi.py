import pexpect
import sys
import re
#from termcolor import colored, cprint


class Ruckus:

    status = None
    def __init__(self, ipAddress, userName, passWord, firstTime=False):
        self.password = passWord
        try:
            child = pexpect.spawn(
                'ssh  -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + ipAddress)
            child.delaybeforesend = 1
            child.expect('Please login:')
            child.sendline(userName)
            child.expect('password :')
            child.sendline(passWord)
            # Handle different expected responses
            index = child.expect(['rkscli:', 'New password:'])

            if index == 0:
                # Successfully logged in
                print("Logged in successfully")
            elif index == 1:
                # Password change required
                new_password = 'n3tw0rks.'
                child.sendline(new_password)
                child.expect('Confirm password:')
                child.sendline(new_password)
                child.expect('Please login:')
                child.sendline(userName)
                child.expect('password :')
                child.sendline(new_password)
                child.expect('rkscli:')
                self.password = new_password
            self.child = child
            print('connected to: '+ipAddress)
            self.status = 1
        except KeyboardInterrupt:
            # On Cntl-C
            self.status = 0
        except pexpect.TIMEOUT:
            print("scan: pexpect.TIMEOUT")
            pass
        except pexpect.EOF:
            self.status = 0
            #print("scan: exception: {0} ".format(sys.exc_info()[0]))
            print('Error al conectar a '+ipAddress)

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
            # print(lista)
            return lista

    def parse_lines(self, raw_data):
        lista = {}
        for line in re.split(r"[~\r\n]+", raw_data):
            if ':' not in line:
                print(line)
                continue			
            key_value = re.split(":", line)
            #value = line.split(':', maxsplit=1)[1].strip()
            lista = {key_value[0].strip():key_value[1].strip()}
            print(lista)
            # if line.startswith('SSID'):
        return lista
    '''
	def getEth(self):
		self.child.sendline ('get eth1x supplicant')
		self.child.expect ('rkscli:')
		deviceData = self.child.before
		lines = re.split(r"[~\r\n]+", deviceData.decode("utf-8"))
		for line in lines:
			if re.search('Identity', line):
				columns = re.split(' : ', line)
				return columns[1]
    '''

    def get_clients(self):
        deviceData = self.sendCommand('get wlanlist')
        if deviceData != 0:
            lines = re.split(r"[~\r\n]+", deviceData.decode("utf-8"))
            wlansUp = []
            linesCount = 0
            for line in lines:
                if re.search('up', line):
                    columns = re.split('\s+', line)
                    wlansUp.append(columns[3])
            return wlansUp
        else:
            return []

    def searchVlan(self, interface="", interfacesData=""):
        lines = re.split(r"[~\r\n]+", interfacesData.decode("utf-8"))
        for line in lines:
            columns = re.split('\s+', line)
            if re.match(interface, columns[0]):
                vlan = columns[4]
                return vlan

    def sendCommand(self, command):
        try:
            self.child.sendline(command)
            self.child.expect('rkscli:')
            deviceData = self.child.before
            # print(deviceData)
            #print('*******************send command********************')
            return deviceData
        except pexpect.EOF as identifier:
            return '0'

    def getStations(self, wlan):
        if wlan:
            string_stations = self.sendCommand('get station '+wlan+' list')
            lines = re.split(r"[~\r\n]+", string_stations.decode("utf-8"))
            stations = []
            countStations = 0
            for line in lines:
                columns = re.split('\s+', line)
                if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", columns[0]):
                    countStations = countStations+1
                    station_info = {'mac': columns[0], 'rsi': columns[1],
                                    'vlan': columns[2], 'id': columns[4], 'channel': columns[3]}
                    stations.append(station_info)
            return stations, countStations

    def getDeviceUptime(self):
        deviceName = self.sendCommand('get uptime')
        deviceData = self.parse(deviceName.decode("utf-8"))
        return deviceData

    def getInterfaces(self):
        deviceData = self.sendCommand('get interface')
        return deviceData

    def getDeviceName(self):
        # prueba de funcion get_version # borrar!!!
        #self.get_version()
        deviceName = self.sendCommand('get device-name')
        if deviceName != 0:
            # print(deviceName)
            deviceData = self.parse(deviceName.decode("utf-8"))
            return deviceData
        else:
            return 0

    def getVersion(self):
        raw_data = self.sendCommand('get version')
        if raw_data != 0:
            deviceVersion = self.parse_lines(raw_data)
        #print(deviceVersion)
        return deviceVersion['Version']
        
    def getDeviceLocation(self):
        deviceLocation = self.sendCommand('get device-location')
        deviceData = self.parse(deviceLocation.decode("utf-8"))
        return deviceData

    def getWlan(self, wlanInterface):
        wlanData = self.sendCommand('get encryption '+wlanInterface)
        DeviceInterfaces = self.getInterfaces()
        vlan = self.searchVlan(wlanInterface, DeviceInterfaces)
        deviceData = self.parse(wlanData.decode("utf-8"), wlanInterface, vlan)
        return deviceData

    def reboot(self, host):
        reboot = self.sendCommand('reboot')
        return "ok"

    def setController(self):
        controller = self.sendCommand('set scg ip 192.168.188.10')
        return controller

    def getData(self):
        deviceLocation = self.sendCommand('get boarddata')
        deviceData = self.parse(deviceLocation.decode("utf-8"))
        mac_address = re.split('base', deviceData['V54 MAC Address Pool'])
        data = {
            'mac address':mac_address[1],
            'serial':deviceData['Serial#'],
            'model':deviceData['Model'],
            'version':deviceData['rev'],
            }        
        return data
        

    def getAll(self, host):
        newdict = []
        post = {}
        hostName = self.getDeviceName()
        hostLocation = self.getDeviceLocation()
        hostUptime = self.getDeviceUptime()
        #hostMacEth = self.getEth()
        wlans = self.getWlanList()
        for wlan in wlans:
            wlanJson, countStations = self.getWlan(wlan)
            newdict.append(wlanJson)

        post["interfaces"] = newdict
        post["hostname"] = hostName
        post["hostlocation"] = hostLocation
        post["ipv4"] = host
        post["hostUptime"] = hostUptime
        #post["mac_eth"] = hostMacEth
        post["status"] = 1

        return post

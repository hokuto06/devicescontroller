import routeros_api

class Mikrotik:

    status = None

    def __init__(self, ipAddress, userName, passWord):
        self.password = passWord
        connection = routeros_api.RouterOsApiPool(ipAddress, userName, passWord)
        api = connection.get_api()
        self.api = api
        self.status = 1
    
    def get_clients(self):
        list_dhcp = self.api.get_resource('/ip/dhcp-server/lease')
        dhcp_list = list_dhcp.get(server="dhcp1")
        list_client = []
        for dhcp_client in dhcp_list:
            if 'mac-address' in dhcp_client and dhcp_client['mac-address']:
                list_client.append({
                    'address':dhcp_client['address'],
                    'mac':dhcp_client['mac-address'],
                    'server':dhcp_client['server']
                    })
        return list_client

    def getDeviceName(self):
        identity = self.api.get_resource('/system/identity')
        _identity = identity.get()
        return _identity[0]['name']

    def getData(self):
        routerboard = self.api.get_resource('/system/routerboard')
        interfaces = self.api.get_resource('/interface/ethernet')
        _routerboard = routerboard.get()
        for interface in interfaces.get():
            if interface['name']=='ether1':
                mac_address=interface['mac-address']
        version =_routerboard[0]['current-firmware']
        model =_routerboard[0]['model']

        data = {
            'mac address':mac_address,
            # 'serial':deviceData['Serial  #'],
            'model':model,
            'version':version,
            }        
        return data
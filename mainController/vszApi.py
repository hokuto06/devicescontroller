import RuckusVirtualSmartZoneAPIClient
import json

class connectVsz():
    def __init__(self, ipAddress, userName, passWord):
        try:
            client = RuckusVirtualSmartZoneAPIClient.Client()
            client.connect(url='https://54.85.134.165:8443', username='admin', password='elrbsestNF!25')
            self.client = client
            self.mac_address = '2C:C5:D3:2F:33:50'
            self.status = 1
        except Exception as e:
            print(e)

    # response = client.get(method='/rkszones')
    # print(json.dumps(response.json(), indent=4))

    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')

    #cambia nombre de dispositivo.

    def search_ap(self):
        response = self.client.get(method='/aps/'+self.mac_address)
        # print(response.status_code) # --> 204
        if response == 204:
            return('ok')

    def config_ap(self):
        hostname = "prueba"
        ip_address = "10.6.255.10"
        mac_address = "2C:C5:D3:2F:33:50"
        description = "ap prueba"
        response = self.client.put(method=f'/aps/'+mac_address, data={ "name":hostname,
                                                                      "description":description,
                                                                      "network":{
                                                                        "ipType": "Static",
                                                                        "ip": ip_address,
                                                                        "netmask": "255.255.255.0",
                                                                        "gateway": "10.6.255.1",
                                                                        "primaryDns": "10.6.255.1"
                                                                      },
                                                                          "apMgmtVlan": {
                                                                            "id": "1",
                                                                            "mode": "USER_DEFINED"                                                                
                                                                        }
                                                                })

    results = (json.dumps(response.json(), indent=4))
    print(results)

    self.client.disconnect()
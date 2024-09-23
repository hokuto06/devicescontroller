import RuckusVirtualSmartZoneAPIClient
import json
 
class connectVsz():
    def __init__(self, vsz_ip):
        try:
            client = RuckusVirtualSmartZoneAPIClient.Client()
            client.connect(url='https://'+vsz_ip+':8443', username='admin', password='elrbsestNF!25')
            # client.connect(url='https://192.168.188.10:8443', username='admin', password='elrbsestNF!25')
            self.client = client
            # self.mac_address = mac_address
            self.status = 1
        except Exception as e:
            print(e)
 
    # response = client.get(method='/rkszones')
    # print(json.dumps(response.json(), indent=4))
 
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')
 
    #cambia nombre de dispositivo.
 
    def get_ap_info(self, mac_address):
        response = self.client.get(method='/aps/'+mac_address)
        if response.status_code == 200:
            results = (json.dumps(response.json(), indent=4))
            return results
 
 
    def search_ap(self,mac_address):
        print(mac_address)
        response = self.client.get(method='/aps/'+mac_address)
        # print(response.status_code) # --> 204
        print(response.status_code)
        if response.status_code == 200:
            return('ok')
        else:
            return('no')
 
    def config_ap(self,mac_address,hostname, ip_address, description):
        # response = {"name":hostname,"descripcion":description,"mac_address":mac_address,"network":{"ip":ip_address}}
        print('mac address: '+mac_address)
        print('ip address: '+ip_address)
 
        response = self.client.put(method=f'/aps/'+mac_address, data={ "name":hostname,
                                                                      "description":description,
                                                                      "network":{
                                                                        "ipType": "Static",
                                                                        "ip": ip_address,
                                                                        "netmask": "255.255.252.0",
                                                                        "gateway": "192.168.112.1",
                                                                        "primaryDns": "192.168.112.1"
                                                                      },
                                                                        "apMgmtVlan": {
                                                                            "id": 100,
                                                                            "mode": "USER_DEFINED"
                                                                         }
                                                                })
        print(response)
        # results = (json.dumps(response.json(), indent=4))
        # print(results)
 
    def desconnect(self):
        self.client.disconnect()
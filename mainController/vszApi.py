import RuckusVirtualSmartZoneAPIClient
import json

class connectVsz():
    def __init__(self):
        try:
            client = RuckusVirtualSmartZoneAPIClient.Client()
            client.connect(url='https://192.168.188.10:8443', username='admin', password='elrbsestNF!25')
            # client.connect(url='https://vsz.gocloud1.com:8443', username='admin', password='elrbsestNF!25')
            # client.connect(url='https://192.168.73.3:8443', username='admin', password='Lcdsnlsll1.')
            self.client = client
            self.status = 1
        except Exception as e:
            print(e)

    # response = client.get(method='/rkszones')
    # print(json.dumps(response.json(), indent=4))

    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
    # response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')

    #cambia nombre de dispositivo.

    def get_aps_from_vsz(self):
        response = self.client.get(method='/aps/')
        if response.status_code == 200:
            # results = (json.dumps(response.json(), indent=4))
            results = response.json()
        else:
            results = "ok"
        return results 

    def get_ap_info(self, mac_address):
        response = self.client.get(method='/aps/'+mac_address)
        if response.status_code == 200:
            results = (json.dumps(response.json(), indent=4))
            return results


    def search_ap(self, mac_address):
        response = self.client.get(method='/aps/'+mac_address)
        # print(response.status_code) # --> 204
        print(response.status_code)
        if response.status_code == 200:
            return('ok')
        else:
            return('no')

    def config_ap(self,mac_address, hostname, ip_address, description):
        mac_address = self.mac_address
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

    def config_ap_hostname(self,mac_address, hostname):
        # response = {"name":hostname,"descripcion":description,"mac_address":mac_address,"network":{"ip":ip_address}}
        print('mac address: '+mac_address)
        response = self.client.put(method=f'/aps/'+mac_address, data={ "name":hostname})
        print(response)

    def get_zones(self):
        response = self.client.get(method='/rkszones')
        # zones_list = json.dumps(response.json(), indent=4)
        zones_list = response.json()
        return zones_list['list']

    def get_groups(self):
        response = self.client.get(method='/rkszones/900ffa67-d780-4dc0-bc0c-0c5d7a32662f/apgroups/')
        groups_list = response.json()
        return groups_list['list']

    def desconnect(self):
        self.client.disconnect()
import RuckusVirtualSmartZoneAPIClient
import json

client = RuckusVirtualSmartZoneAPIClient.Client()
client.connect(url='https://54.85.134.165:8443', username='admin', password='elrbsestNF!25')

# response = client.get(method='/rkszones')
# print(json.dumps(response.json(), indent=4))

# response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
# response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')
response = client.get(method='/aps/2C:C5:D3:2F:33:50')

#cambia nombre de dispositivo.

hostname = "prueba"
ip_address = "10.6.255.10"
mac_address = "2C:C5:D3:2F:33:50"
description = "ap prueba"
# response = client.put(method=f'/aps/'+mac_address, data={ "name":hostname,
                                                                # "description":description,
#                                                               "network":{
#                                                             "ipType": "Static",
#                                                             "ip": ip_address,
#                                                             "netmask": "255.255.255.0",
#                                                             "gateway": "10.6.255.1",
#                                                             "primaryDns": "10.6.255.1"
#                                                               },
#                                                                   "apMgmtVlan": {
#                                                                     "id": "1",
#                                                                     "mode": "USER_DEFINED"                                                                
#                                                                 }
#                                                         })

results = (json.dumps(response.json(), indent=4))
print(response.status_code) # --> 204
print(results)

client.disconnect()

"""
{
    "id": "b4187899-38ae-4ace-8e40-0bc444455156",
    "name": "Staging Zone"
},
"""
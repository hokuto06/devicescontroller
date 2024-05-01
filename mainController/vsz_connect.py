import RuckusVirtualSmartZoneAPIClient
import json

client = RuckusVirtualSmartZoneAPIClient.Client()
client.connect(url='https://54.85.134.165:8443', username='admin', password='elrbsestNF!25')

# response = client.get(method='/rkszones')
# print(json.dumps(response.json(), indent=4))

# response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0')
# response = client.get(method='/rkszones/28b9296d-7dc9-44d9-9221-80a926f1f4a0/apgroups/4066127f-a6ed-4a26-8951-dab89c95d216')
#response = client.get(method='/aps/34:20:E3:13:39:D0')

#cambia nombre de dispositivo.
response = client.put(method=f'/aps/34:20:E3:13:39:D0', data={"name":"BUESCAP713"})
#results = (json.dumps(response.json(), indent=4))
print(response.status_code) # --> 204
#print(results)

client.disconnect()
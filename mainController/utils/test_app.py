from unifiApi import Unifi

unifi = Unifi('10.2.2.30', 'n1mbu5','n3tw0rks')
data = unifi.getData()
print(data)
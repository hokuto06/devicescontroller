import rssi
from pprint import pprint
ifc = 'wlo1'
rssi_scan = rssi.RSSI_Scan(ifc)
rssi_loc = rssi.RSSI_Localizer(ifc)

ssids = ['Marriott']

ap_info = rssi_scan.getAPinfo(networks=ssids, sudo=True)
# scan = rssi_scan.getRawNetworkScan(sudo=True)
distance = rssi_loc.getDistanceFromAP()
# pprint(scan)
pprint(ap_info)
pprint(distance)
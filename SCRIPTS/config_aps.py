import sys 
import os 

sys.path.append('/home/hokuto/devicescontroller/mainController')

from unifiApi import Unifi
from tools import unifi_controller


def get_devices():
    unifi_controller('172.20.197.148','etw7f5dj')


def set_ap_default(ip_address, user, password):
    device = Unifi(ip_address, user,password)
    command = device.sendCommand('mca-cli-op set-default\n')
    print(command)

def set_ap_controller(ip_address, user, password):
    device = Unifi(ip_address, user, password)
    device.set_inform('172.20.197.148')
    print('ok')

# set_ap_controller('10.10.7.40','ubnt','ubnt')
get_devices()
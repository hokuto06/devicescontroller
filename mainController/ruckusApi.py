import pexpect
from pexpect import popen_spawn
# from netmiko import ConnectHandler
import sys
import re

class Ruckus:
    def __init__(self, ipAddress, userName, passWord):
        status = None
        try:
            child = pexpect.popen_spawn.PopenSpawn(
                'ssh  -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + ipAddress)
            child.delaybeforesend = 1
            child.expect('Please login:')
            child.sendline(userName)
            child.expect('password :')
            child.sendline(passWord)
            child.expect('rkscli:')
            self.child = child
            print('connected to: '+ipAddress)
            self.status = 1
        except KeyboardInterrupt:
            # On Cntl-C
            pass
        except pexpect.TIMEOUT:
            print("scan: pexpect.TIMEOUT")
            pass
        except pexpect.EOF as o:
            self.status = 0
            print(o)
            print('Error al conectar a '+ipAddress)


        # devices = {
        #     "device_type": "ruckus_fastiron",
        #     "ip": "192.168.188.62",
        #     "username": "n1mbu5",
        #     "password": "n3tw0rks",
        # }
        # ssh = ConnectHandler(**devices)
        # print(ssh)
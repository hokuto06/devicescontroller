import sys, re
import argparse
import paramiko
import warnings
from paramiko.client import SSHClient, AutoAddPolicy, RejectPolicy
from paramiko.ssh_exception import SSHException

warnings.filterwarnings(action='ignore',module='.*paramiko.*')

class Unifi:
	status = None

	def __init__(self, ipAddress, userName, passWord):
		try:
			print(f'Intentando conectar a {ipAddress} como {userName}')
			client = paramiko.SSHClient()
			# client.load_system_host_keys()
			client.set_missing_host_key_policy(AutoAddPolicy)
			client.connect(ipAddress, port=22, username=userName, password=passWord)
			self.client = client
			self.status = 1
		except paramiko.ssh_exception.AuthenticationException:
			#no_connetion_list.append(ipAddress)
			print("Error al autenticar en "+ipAddress)
			#print(e)
			self.status = 2
	
		except paramiko.ssh_exception.NoValidConnectionsError:
			#print (e)
			self.status = 3
			print("Conexion invalida a "+ipAddress)
			#return "No se ha podido establecer la conexion"
		except SSHException as sshException:
			print(sshException)
		#finally:
			#client.close()
			#return ipAddress+ " comando aplicado"
	def close(self):
		self.client.close()

	def reboot(self):
		#data = self.sendCommand('reboot\n')
		#data = self.sendCommand('a=0\nwhile [ $a -lt 399 ];do ifconfig wifi1 down\nifconfig wifi0 down;sleep 1;a=`expr $a + 1`;done\n')
		self.create_file()
		#self.make_exec()
		self.make_crond()
		self.close()
		return "ok"

###############################
	def make_crond(self):
		values = open("unifi/ash.sh", "r").read()
		values = values.split("\n")
		freq = values[0]
		start_run = values[1]
		end_run = values[2]
		killed_time_min = values[3]
		killed_time_hr = values[4]
		#command = 'crontab -r;[[ -f /usr/sbin/mc-dump.sh ]] && (crontab -l ; echo "*/'+str(freq+)' '+start_run+'-'+end_run+' * * * /usr/sbin/mc-dump.sh run") | crontab -;(crontab -l ; echo "'+killed_time_min+' '+killed_time_hr+' * * * /usr/sbin/mc-dump.sh finish") | crontab -;crond enable'
		command = ""
		stdin, stdout, stderr = self.client.exec_command(command)
		#z=stdout.read()

	def create_file(self):
		file_content = open('unifi/script.sh', 'r').read()
		command = ('echo \''+file_content+'\' > /usr/sbin/mc-dump.sh && chmod +x /usr/sbin/mc-dump.sh')
		stdin, stdout, stderr = self.client.exec_command(command)
		#stdin, stdout, stdeer = unifi.exec_command(command)
		print(stdout)
		print(stderr)

###############################

	def sendCommand(self, command):
		stdin, stdout, stderr = self.client.exec_command(command)
		output = stdout.read().decode('ascii')
		error = stderr.read().decode('ascii')
		if output:
			return output
		else:
			return error

	def getData(self):
		data = self.sendCommand('mca-cli-op info\n')
		_data = self.parserData(data)
		_lower_data = {k.lower(): v for k, v in _data.iteritems()}
		return _lower_data

	def getDeviceName(self):
		name = self.getData()
		return(name['Hostname'])

	def getWlanClients(self):
		data = self.sendCommand('wlanconfig ath0 list station\n')
		# data = self.sendCommand('wlanconfig ath1 list station\n')
		# data = self.sendCommand('wlanconfig ath2 list station\n')
		reg_lines = re.split(r"[~\r\n]+", data)
		lista = []
		for i in range(2, len(reg_lines)-1):
			lines = reg_lines[i].split()
			lista.append({"mac":lines[0]})
		#_data = [self.parserData(data)]
		return lista

	def set_inform(self, ip_controller):
		_data = self.sendCommand('mca-cli-op set-inform http://'+ip_controller+':8080/inform')
		return _data

	def parserData(self, data):
		lines = re.split(r"[~\r\n]+", data)
		lista = {}
		linesCount = 0
		for line in lines:
			if re.search(':', line):
				linesCount = linesCount+1
				_list = line.split(":", 1)
				rawn_data = _list[0].lstrip().strip()
				key = rawn_data.lower()
				#key = _list[0].lstrip().strip()
				value = _list[1].lstrip().strip()
				lista[key] = value
		if linesCount==1:
			lista = value
		return lista
	
	def check_connection(self):
		try:
			self.client.exec_command('ls\n', timeout=5)
			return True
		except Exception as e:
			print("Connection lost : %s" %e)
			return False
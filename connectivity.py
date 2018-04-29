import subprocess
from subprocess import call, PIPE, STDOUT
import shlex
import time

def get_return_code (cmd, stderr=STDOUT):
	args = shlex.split(cmd)
	return call(args, stdout=PIPE, stderr=stderr)
	
def check_connectivity ():
	cmd = 'ping -c 1 8.8.8.8'
	return get_return_code(cmd) == 0

def main ():
	while True:
		if check_connectivity () == False:
			print ('Internet is down... killing any existing OpenVPN process.')
			# killall OpenVPN
			proc = subprocess.Popen(['sudo', 'killall', 'openvpn'])
			print ('Restarting the OpenVPN process...')
			# Restart OpenVPN client
			proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'], stdout=subprocess.PIPE)
			print ('OpenVPN restarted successfully!')
		else:
			print ('Internet is up.')
		time.sleep (600)

main ()
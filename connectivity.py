import socket
import subprocess
import time

def check_connectivity (host="8.8.8.8", port=53, timeout=3):
	"""
	Host: 8.8.8.8 (google-public-dns-a.google.com)
	OpenPort: 53/tcp
	Service: domain (DNS/TCP)
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		return False

def main ():
	while True:
		if check_connectivity () == False:
			print ('Internet is down... killing OpenVPN process.')
			# killall openvpn
			proc = subprocess.Popen(['sudo' 'killall' 'openvpn'])
			print ('Restarting the OpenVPN process...')
			# Restart OpenVPN client
			proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'], stdout=subprocess.PIPE)
			print ('OpenVPN restarted successfully!')
		else:
			print ('Internet is up.')
		time.sleep (10)

main ()
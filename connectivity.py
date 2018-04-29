import socket
import subprocess

def check_connectivity (host="8.8.8.8", port=53, timeout=3):
	"""
	Host: 8.8.8.8 (google-public-dns-a.google.com)
	OpenPort: 53/tcp
	Service: domain (DNS/TCP)
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		print ('Internet up!')
		return True
	except Exception as ex:
		print ('Internet down!')
		return False

def main ():
	# Start OpenVPN
	proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'], stdout=subprocess.PIPE)
	while True:
		if check_connectivity () == False:
			print ('Internet is down')
			# killall openvpn
			proc = subprocess.Popen(['killall openvpn'])
			# Restart OpenVPN client
			proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'], stdout=subprocess.PIPE)
		else:
			print ('Internet is up!')
		sleep (10)



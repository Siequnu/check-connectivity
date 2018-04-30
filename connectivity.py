import subprocess
from subprocess import call, PIPE, STDOUT
import shlex
import time
import sys
import arrow

# Global variables
LAST_VPN_RESTART = False

# Get the return code of an externally run process
def get_return_code (cmd, stderr=STDOUT):
	args = shlex.split(cmd)
	return call(args, stdout=PIPE, stderr=stderr)
	
# Run a ping check and return exit code
def check_connectivity ():
	cmd = 'ping -c 1 8.8.8.8'
	return get_return_code(cmd) == 0

# Main entrance to program
def main (sleep_time_secs = 20):
	global LAST_VPN_RESTART
	
	while True:
		if check_connectivity () == False:
			print ('Internet is down... killing any existing OpenVPN process.')
			# killall OpenVPN
			proc = subprocess.Popen(['sudo', 'killall', 'openvpn'])
			time.sleep(10)
			print (str(proc))
			print ('Restarting the OpenVPN process...')
			# Restart OpenVPN client
			proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'])
			print (str(proc))
			print ('OpenVPN restarted successfully!')
			LAST_VPN_RESTART = arrow.now()
		else:
			print ('Internet is up.')
			if LAST_VPN_RESTART:
				print ('Last VPN restart was ' + str(LAST_VPN_RESTART.humanize()) + ' , at: ' + str(LAST_VPN_RESTART))
		time.sleep (sleep_time_secs)

# Get sleep time argument, if present in arguments
print ('Starting connectivity manager...')
if len(sys.argv) > 1:
	sleep_time_secs = sys.argv[1]
	print ('Setting sleep time as ' + str(sleep_time_secs))
	main (int(sleep_time_secs))
else:
	main()
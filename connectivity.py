import subprocess
from subprocess import call, PIPE, STDOUT
import shlex
import time
import sys
import arrow
from termcolor import colored

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
			print colored ('Internet is down... killing any existing OpenVPN process.', 'yellow')
			# killall OpenVPN
			proc = subprocess.Popen(['sudo', 'killall', 'openvpn'])
			time.sleep(10)
			print (str(proc))
			print colored ('Restarting the OpenVPN process...', 'yellow')
			# Restart OpenVPN client
			proc = subprocess.Popen(['sudo','/usr/sbin/openvpn','--config',
							 '/etc/openvpn/us15udp.conf', '--auth-user-pass',
							 '/etc/openvpn/auth.txt'])
			print (str(proc))
			print colored ('OpenVPN restarted successfully!', 'yellow')
			LAST_VPN_RESTART = arrow.now()
		else:
			print colored ('Internet is up.', 'yellow')
			if LAST_VPN_RESTART:
				print colored ('Last VPN restart was ' + str(LAST_VPN_RESTART.humanize()) + ', at: ' + str(LAST_VPN_RESTART.format('YYYY-MM-DD HH:mm:ss')), 'yellow')
		time.sleep (sleep_time_secs)

# Main program start
print colored ('Starting connectivity manager...', 'yellow')

# Get sleep time argument, if present in arguments
if len(sys.argv) > 1:
	sleep_time_secs = sys.argv[1]
	print colored ('Setting sleep time as ' + str(sleep_time_secs), 'yellow')
	main (int(sleep_time_secs))
else:
	main()
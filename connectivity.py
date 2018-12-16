"""OpenVPN Connectivity Manager.

Usage:
  connectivity.py <openvpn-executable> <openvpn-config> <openvpn-authuserpass> [--s <sleep-time>]
  connectivity.py (-h | --help)
  connectivity.py --version

Options:
  -h --help     Show this screen.
  --s           Sleep time in seconds [default: 20].
  --version     Show version.

"""
from docopt import docopt

import subprocess
from subprocess import call, PIPE, STDOUT
import shlex
import time
import sys
import arrow
from termcolor import colored
import random

# Global variables
LAST_VPN_RESTART = False

# Get the return code of an externally run process
def get_return_code (cmd, stderr=STDOUT):
	args = shlex.split(cmd)
	return call(args, stdout=PIPE, stderr=stderr)
	
# Run a ping check and return exit code
def check_connectivity ():
	cmd = 'ping -c 1 172.217.160.78' # Google.com IP
	return get_return_code(cmd) == 0

# Get a master list of working servers
def get_server_list (openvpn_config):
	with open(openvpn_config) as f:
		content = f.readlines()
		content = [x.strip() for x in content]
		return content
		
def get_random_server (openvpn_config):
	servers = get_server_list(openvpn_config)
	return random.choice(servers)
	

# Main entrance to program
def main (openvpn_executable, openvpn_config, openvpn_authuserpass, sleep_time_secs = 600):
	global LAST_VPN_RESTART
	
	while True:
		if check_connectivity () == False:
			# killall OpenVPN
			print colored ('Internet is down... killing any existing OpenVPN process.', 'yellow')
			subprocess.Popen(['sudo', 'killall', 'openvpn'])
			time.sleep(5)
			
			# Get random server from config list
			random_config = get_random_server(openvpn_config)
			print colored ('Connecting to ' + random_config + '...', 'blue')
			
			# Restart OpenVPN client
			print colored ('Restarting the OpenVPN process...', 'yellow')
			subprocess.Popen(['sudo',openvpn_executable,'--config',
							 random_config, '--auth-user-pass',
							 openvpn_authuserpass])				 
			time.sleep (60)
			
			# Check restart was successful
			if check_connectivity() == True:
				print colored ('OpenVPN restarted successfully!', 'yellow')
				LAST_VPN_RESTART = arrow.now()
			else:
				print colored ('OpenVPN did not successfully restart!', 'red')
				print colored ('Sleeping for ' + str(sleep_time_secs) + ' seconds.', 'yellow')
		else:
			print colored ('Internet is up.', 'yellow')
			if LAST_VPN_RESTART:
				print colored ('Last VPN restart was ' + str(LAST_VPN_RESTART.humanize()) + ', at: ' + str(LAST_VPN_RESTART.format('YYYY-MM-DD HH:mm:ss')), 'yellow')
		time.sleep (sleep_time_secs)


# Main program start
arguments = docopt(__doc__, version='OpenVPN Connectivity Manager 2.0')
print colored ('Starting OpenVPN Connectivity Manager...', 'yellow')

# Assign arguments
openvpn_executable = arguments['<openvpn-executable>']
openvpn_config = arguments['<openvpn-config>']
openvpn_authuserpass = arguments['<openvpn-authuserpass>']
if '<sleep-time>' in arguments:
	sleep_time_secs = int(arguments['<sleep-time>'])
	print colored ('Setting sleep time as ' + str(sleep_time_secs), 'yellow')
	main (openvpn_executable, openvpn_config, openvpn_authuserpass, sleep_time_secs)
else:
	main (openvpn_executable, openvpn_config, openvpn_authuserpass)

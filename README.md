# check-connectivity
Python script to manage OpenVPN connectivity 

When running OpenVPN on always-on boxes, the process sometimes hangs without restarting. 
This script designed to ping a given host to automatically restart a hanging OpenVPN client process.

## How It Works

This simple python script manages OpenVPN connections via subprocess Popen commands. A domain
is pinged based on a given time interval to check connectivity status. If the internet connection
is down, the script kills all OpenVPN processes, and restarts a new process.

## Usage

First, install the following dependencies: `docopt`, `termcolor`, and `arrow`:

```sh
$ pip install docopt termcolor arrow
```

Usage is:

```sh
$ python connectivity.py <openvpn-executable> <openvpn-config> <openvpn-authuserpass> [--s <sleep-time>]
```

A general use case might be:

```sh
$ python connectivity.py /usr/sbin/openvpn /etc/openvpn/vpn.conf /etc/openvpn/auth.txt --s 40
```

## Usage

The script accepts the following command line arguments:

* **<openvpn-executable>**: relative path to the OpenVPN executable.
* **<openvpn-config>**: relative path to the OpenVPN configuration file.
* **<openvpn-authuserpass>**: relative path to the OpenVPN password file. This is necessary to automate
	the reconnection if prompted for username and password.

The following optional arguments may be given:

* **--s <sleep-time>**: the sleep time between checking internet status. Sending `--s 20`
	will ping the internet once every 20 seconds. The default value (if not set) is 600 seconds.
	
* **-v**: show the version number.


## Dependencies

The following third-party libraries are used:

`docopt`: provides a clean way to generate a help document and accept CLI args;

`termcolor`: easy way to write colour into term;

`arrow`: convenient way to manipulate dates and times
#!/usr/bin/env python3

# Archicad Python JSON API Connection Test
# BORSH, 2023

import sys
import urllib.request
import json


# App details
APP_TITLE = 'Archicad Python JSON API Connection Test'
APP_CODE = 'archiconnect'
APP_DESC = 'Connects to Archicad Python JSON API and shows Archicad host info.'
APP_AUTHOR = 'GAG'
APP_COMPANY = 'BORSH'
APP_URL = 'https://borsh.pro'
APP_VER = '27.1.2.0'


# Default Archicad server address and ports range
AC_HOST_DEFAULT = '127.0.0.1'
AC_PORT_DEFAULT = 19723
AC_PORTS = (19723, 19744)

AC_CMD_SAMPLES = (
	"GetActivePenTables",
	"GetAllClassificationSystems",
	"GetAllElements",
	"GetAllPropertyNames",
	"GetClassificationSystemIds",
	"GetProductInfo",
	"GetPublisherSetNames",
	"IsAlive"
)


def info():
	"""
	Shows app information.
	"""

	print(f'{APP_TITLE} [{APP_CODE}]')
	print(f'Version: {APP_VER}')
	print(f'Created by {APP_AUTHOR}\n{APP_URL}\n')
	print(f'Description:\n{APP_DESC}\n')


def usage():
	"""
	Shows app usage.
	"""

	print('\nUSAGE:')
	print(f'./{APP_CODE}.py ADDRESS PORT COMMAND\n')
	print('\tADDRESS\n\t\tNetwork name or IP address of Archicad host.')
	print(f'\t\tDefault address: {AC_HOST_DEFAULT}')
	print('\tPORT\n\t\tPort of Archicad host.')
	print(f'\t\tDefault ports range: {AC_PORTS[0]}—{AC_PORTS[1]}')
	print('\tCOMMAND\n\t\tCustom Archicad API command to execute.')
	print('\t\tAccepted commands without parameters:')
	for cmd in AC_CMD_SAMPLES:
		print(f'\t\t\t{cmd}')
	print('\nUSAGE EXAMPLES:')
	print(f'./{APP_CODE}.py localhost {AC_PORT_DEFAULT}')
	print(f'./{APP_CODE}.py {AC_HOST_DEFAULT} {AC_PORT_DEFAULT} {AC_CMD_SAMPLES[1]}\n\n')


def print_json(msg: str | dict, title: str | None = None):
	"""
	Prints formatted dict as JSON
	"""

	if title is not None:
		print(f'\n{title}:\n')
	print(json.dumps(msg, ensure_ascii=False, indent='\t'))


def print_err(err: dict | None) -> None:
	"""
	Prints API error.
	"""

	if err is None:
		return
	print(f'Error {err["code"]}\n\t{err["message"]}\n')


def get_ac_ports_range() -> range:
	"""
	Gets the Archicad Python API ports range.
	"""

	return range(AC_PORTS[0], AC_PORTS[1], 1)


def connect_host(addr: str | None = None, port: int | str | None = None, debug: bool = False) -> urllib.request.Request:
	"""
	Creates request to Archicad host.
	There is no actual request being sent at this time.
	"""

	if addr is None:
		addr = AC_HOST_DEFAULT

	if port is None:
		port = AC_PORT_DEFAULT

	address = f'http://{addr}:{port}'
	if debug:
		# print(f'Address: {address}')

		if port not in get_ac_ports_range():
			print('WARNING: Port is not in default range.\n')

	req = urllib.request.Request(address)
	req.add_header('Content-Type', 'application/json')
	return req


def api_cmd(req: urllib.request.Request, cmd: str, timeout: int = 2, debug: bool = False):
	"""
	Executes API command.
	"""

	cmd = '{"command":' + f'"API.{cmd}"' + '}'

	if debug:
		print(cmd)

	try:
		# Send request
		res = urllib.request.urlopen(req, cmd.encode("utf-8"), timeout=timeout)

	except urllib.error.URLError as e:
		print(f'ERROR: {e.reason}\n')
		return False, None, None

	answer = json.loads(res.read())

	if answer is None:
		return False, None, None

	if debug:
		print_json(answer)

	if 'succeeded' not in answer:
		return False, None, None
	else:
		succeeded = answer['succeeded']

	if not succeeded and 'error' in answer:
		err = answer['error']
		print_err(err)

		return False, None, err

	if not succeeded:
		return False, None, None

	if 'result' in answer:
		result = answer['result']

	return succeeded, result, None


def is_alive(req: urllib.request.Request, debug: bool = False):
	"""
	Gets API status.
	"""

	succeeded, res, err = api_cmd(req, 'IsAlive', debug=debug)
	if succeeded and res is not None:
		return res['isAlive']
	else:
		return False


def get_host_info(req: urllib.request.Request, debug: bool = False):
	"""
	Gets Archicad host info.
	"""

	succeeded, res, err = api_cmd(req, 'GetProductInfo', debug=debug)
	if succeeded and res is not None:
		return res
	else:
		return False


def get_host_version(product):
	"""
	Formats the host version.
	"""

	# print(product)
	return f'Archicad {product["version"]} {product["buildNumber"]} {product["languageCode"]}'


def connect_ac(addr: str | None = None, port: int | str | None = None, debug: bool = False):
	"""
	Connects to Archicad JSON API.
	"""

	req = connect_host(addr, port, debug=debug)

	print(f'Connecting to {req.host} …\n')

	result = is_alive(req, debug=debug)
	print(f'Is alive: {result}')

	if not result:
		if debug:
			print('ERROR: Failed to acquire Archicad port!')
		return None

	result = get_host_info(req, debug=debug)
	host_ver = get_host_version(result)
	print(f'Host version: {host_ver}\n')

	return req


def main(addr: str | None = None, port: int | str | None = None, cmd: str | None = None, debug: bool = False) -> int:

	if addr == '--port':
		# Running inside Archicad
		addr = None

	if addr in AC_CMD_SAMPLES:
		cmd = addr
		addr = None

	# debug = True
	if cmd is None:
		# Show host version
		req = connect_ac(addr, port, debug=debug)

		if req is None:
			print('Connection failed.\n')
			sys.exit(2)
		else:
			sys.exit(0)

	# Execute custom command
	req = connect_host(addr, port, debug=debug)
	succeeded, res, err = api_cmd(req, cmd, debug=debug)
	if succeeded and res is not None:
		print_json(res)
	else:
		# Custom command failed
		print_err(err)
		sys.exit(3)

	sys.exit(0)


if __name__ == '__main__':
	argc = len(sys.argv)
	# print(sys.argv)

	if argc == 1:
		info()
		usage()
		main()

	elif argc == 2:
		# Address
		main(sys.argv[1])

	elif argc == 3:
		# Address, port
		main(sys.argv[1], sys.argv[2])

	elif argc > 3:
		# Address, port, cmd
		main(sys.argv[1], sys.argv[2], sys.argv[3])

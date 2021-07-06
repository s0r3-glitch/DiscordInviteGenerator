import os
import requests
import ctypes
import threading
import time
from colorama import Fore, init
import random
import string
from discord_webhook import DiscordWebhook
from core.localscommands import clear, pause, title
import json

init()

available = 0
taken = 0 
total = 0
errorCodes = [100, 101, 103, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 307, 308, 400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 422, 425, 426, 428, 431, 451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

def start():
    clear()
    global webhookk
    webhookk = ""
    webhookk = input("Webhook: ")
    if webhookk == "":
        print("The value you entered was null. Please try again.")
        pause()
        start()
    elif webhookk == " ":
        print("The value you entered was null. Please try again.")
        pause()
        start()
    clear()



def getProxy():
	global proxList
	global proxList2
	prox = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=no&anonymity=all")
	if prox.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt = prox.text.splitlines()
	proxList = []
	for line in proxyTxt:
		proxList.append(line)
	prox2 = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=yes&anonymity=all")
	if prox2.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt2 = prox2.text.splitlines()
	proxList2 = []
	for line in proxyTxt2:
		proxList2.append(line)
	

def main():
	getProxy()
	while True:
		thread = threading.Thread(target=checkInvite, daemon=True)
		thread.start()
		time.sleep(0.1)

def checkInvite():
	global taken
	global available
	global total
	global randProxy
	global randProxySSL
	randProxy = random.choice(proxList)
	randProxySSL = random.choice(proxList2)
	lowerLetters = string.ascii_lowercase
	upperLetters = string.ascii_uppercase
	digits = string.digits
	randomCode = ''.join(random.choice(lowerLetters + upperLetters + digits) for i in range(8))
	invite = randomCode
	try:
		discordRequest = requests.get(f"https://discord.com/api/v9/invites/{invite}", proxies={"http": randProxy,"https": randProxySSL})
	except Exception as e:
		#print(e)
		return
	if discordRequest.status_code == 200:
		available += 1
		total += 1
		title("Discord Invite Generator/Checker | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.GREEN + f"[+] Invite '{invite}' is valid.")
		prettyObject = json.loads(discordRequest.text)
		prettyJson = json.dumps(prettyObject, indent=2)
		webhook = DiscordWebhook(url=webhookk, content=prettyJson)
		try:
			response = webhook.execute()
		except Exception:
			print(Fore.YELLOW + "Invalid Webhook URL, saving invite to valid.txt")
			with open("available.txt", "a") as f:
				f.writelines(prettyJson + "\n")
	elif discordRequest.status_code == 404:
		taken += 1
		total += 1
		title("Discord Invite Generator/Checker | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.RED + f"[-] Invite '{invite}' is invalid.")
	elif discordRequest.status_code == 429:
		total += 1
		title("Discord Invite Generator/Checker | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] You are being ratelimited, changing proxies.")
		#print(randProxy)
		checkInvite()
	elif discordRequest.status_code in errorCodes:
		total += 1
		title("Discord Invite Generator/Checker | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] An unexpected error has occured. Error Code: " + str(discordRequest.status_code))

def menu():
	title("Discord Invite Generator/Checker | arshan.xyz")
	main()

if __name__ == "__main__":
    start()
    menu()
	

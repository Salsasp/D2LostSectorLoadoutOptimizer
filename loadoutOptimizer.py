import pydest
import asyncio
import playerVault
import destinyweapon
from tkinter import *
from tkinter import ttk
import tkinter as tk
import webbrowser
import LostSector
from requests_oauthlib import OAuth2Session
import json
import threading
from selenium import webdriver


client_id = '44039'
api_key = 'f6777de733f847a5a7c8ab50d357d399'
base_auth_url = 'https://www.bungie.net/en/oauth/authorize'
token_url =  'https://www.bungie.net/platform/app/oauth/token/'
redirect_url = 'https://www.github.com/Salsasp'
get_user_details_endpoint = "https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/"


#function for making gui window
def window():
    root = tk.Tk()
    frame = ttk.Frame(root, padding=20)
    frame.grid()
    ttk.Label(frame, text="Destiny 2 Lost Sector Loadout Recommender").grid(row=0,column=0)
    quitButton = ttk.Button(frame, text="QUIT", command=root.destroy).grid(row=0,column=2,ipadx=0,ipady=0)

    #authorization button
    authStatusLabel = ttk.Label(frame, text="")
    authStatusLabel.grid(row=3,column=1)
    ttk.Label(frame, text="Authorize Bungie Account").grid(row=2,column=0)
    ttk.Button(frame,text="Authorize", command=lambda:openAuthPortal(authStatusLabel)).grid(row=3,column=0)

    #date entry for lost sector
    ttk.Label(frame, text="Enter Date:").grid(row=4, column=0)
    dateEntry = ttk.Entry(frame)
    dateEntry.grid(row=4, column=1)
    ttk.Button(frame, text="submit",command=lambda:dateSubmit(dateErrorMsg, lsNameLabel, lsRewardLabel, lsChampionsLabel, lsSurgeLabel, dateEntry.get())).grid(row=4,column=2)
    dateErrorMsg = ttk.Label(frame, text="Use xx/xx/xxxx format")
    dateErrorMsg.grid(row=4, column=3)
    #TODO: implement error catching for incorrectly formatted dates, or a different date input system, finish authentication process

    #generate loadout button
    primaryWepLabel = ttk.Label(frame, text="")
    primaryWepLabel.grid(row=11, column=0)
    specialWepLabel = ttk.Label(frame, text="")
    specialWepLabel.grid(row=11, column=1)
    heavyWepLabel = ttk.Label(frame, text="")
    heavyWepLabel.grid(row=11, column=2)
    
    #lost sector info
    ttk.Label(frame, text="-- Lost Sector Info --").grid(row=7, column=1, ipadx=10, ipady=10)
    lsNameLabel = ttk.Label(frame, text="Name:")
    lsNameLabel.grid(row=8,column=0)
    lsRewardLabel = ttk.Label(frame,text="Reward:")
    lsRewardLabel.grid(row=8,column=1)
    lsChampionsLabel = ttk.Label(frame,text="Champions:")
    lsChampionsLabel.grid(row=8, column=2)
    lsSurgeLabel = ttk.Label(frame, text="Surge:")
    lsSurgeLabel.grid(row=8,column=3)

    #loadout section
    ttk.Label(frame, text="-- Recommended Loadout --").grid(row=10, column=1, ipadx=10,ipady=10)
    ttk.Button(frame, text="Generate Loadout!", command=lambda: generate(dateErrorMsg, primaryWepLabel, specialWepLabel, heavyWepLabel)).grid(row=9,column=1)

    root.mainloop()

def openAuthPortal(label):
    try:
        driver = webdriver.Firefox
        session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)
        auth_link = session.authorization_url(base_auth_url)
        webbrowser.open_new_tab(auth_link[0])
        redirect_response = input("paste url here") #TODO: start oauth process when tkinter buton is pressed, automatically fetch auth response instead of ctrl c
        session.fetch_token(
            client_id = client_id,
            token_url=token_url,
            authorization_response=redirect_response,
            include_client_id=True
        )
        additional_headers = {'X-API-KEY': api_key}
        response = session.get(url=get_user_details_endpoint, headers=additional_headers)
        responseDict = json.loads(response.text)
        membership_id = responseDict['Response']['membershipId']
        username = responseDict['Response']['uniqueName']
    except BaseException:
        label.config(text="Failed to authorize", foreground="red")
        label.update()
        return
    label.config(text="Authorization success!", foreground="green")
    threading.Thread(
            target=lambda loop: loop.run_until_complete(mainProcess(username, membership_id)),
            args=(asyncio.new_event_loop(),)
        ).start()

async def mainProcess(username, membership_id):

    destiny = pydest.Pydest('f6777de733f847a5a7c8ab50d357d399') #create object to access api using api key

    platform = platforms.get('PC')

    userResponse = await destiny.api.search_destiny_player(platform, username)

    if userResponse['ErrorCode'] == 1 and len(userResponse['Response']) > 0:
        print("---")
        print("Player found!")
        print("Display Name: {}".format(userResponse['Response'][0]['displayName']))
        print("Membership ID: {}".format(userResponse['Response'][0]['membershipId']))
    else:
        print("Could not locate player.")

    vaultData = await destiny.api._get_request("https://www.bungie.net/Platform/Destiny2/"+str(platform)+"/Profile/"+str(userResponse['Response'][0]['membershipId'])+"/?components=102")
    items = vaultData['Response']['profileInventory']['data']['items']
    decodedWeapons = []

    for hash in items:
       dehashedItem = await destiny.decode_hash(hash['itemHash'], 'DestinyInventoryItemDefinition')
       if dehashedItem['itemType'] != 3:
           continue
       powerCap = await destiny.decode_hash(dehashedItem["quality"]["versions"][0]["powerCapHash"], 'DestinyPowerCapDefinition')
       if powerCap["powerCap"] == 1060:
           continue
       decodedWeapons.append(dehashedItem) 
    simplifiedWeapons = generateSimplifiedWeapons(decodedWeapons, destiny)
    global pv 
    pv = playerVault.Vault(vaultData, simplifiedWeapons)
    await destiny.close()

def dateSubmit(dateErrorMsg, label1, label2, label3, label4, date):
    try:
        pv.setDate(date)
        dailysector = LostSector.getSectorByDate(date)
        label1.config(text="Name: " + dailysector.getName())
        label2.config(text="Reward: " + dailysector.getReward())
        label3.config(text="Champions: " + str(dailysector.getChamps()))
        label4.config(text="Surge: " + dailysector.getSurge())
        label1.update()
        label2.update()
        label3.update()
        label4.update()
        dateErrorMsg.config(text="", foreground="black")
    except BaseException:
        dateErrorMsg.config(text="Invalid Date",foreground="red")
        dateErrorMsg.update()
        return


def generate(errorMsg, label1, label2, label3):
    errorMsg.update()
    format = "%m/%d/%Y"
    if(pv.getDate() == ""):
        errorMsg.config(text="Please enter a date",foreground="red")
        errorMsg.update()
        return
    else: errorMsg.config(text="")
    try:
        pv.processWeapons()
        primaryString = "Primary: " + pv.getRecPrimary()
        specialString = "Special: " + pv.getRecSpecial()
        heavyString = "Heavy: " + pv.getRecHeavy()
        label1.config(text=primaryString)
        label2.config(text=specialString)
        label3.config(text=heavyString)
        label1.update()
        label2.update()
        label3.update()
    except AttributeError:
        errorMsg.config(text="Please format correctly",foreground="red")
        errorMsg.update()
        return


damageTypes = {1:'kinetic', 2:'arc', 3:'solar', 4:'void', 6:'stasis', 7:'strand'}
ammoTypes = {1: 'primary', 2: 'special', 3: 'heavy'}
platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}
#seasonal mod list, meaning this will need to be manually changed every season unless I find a reliable data mining source
seasonalChampionMods = {'Auto Rifle': 'barrier', 'Glaive': 'unstoppable', 'Hand Cannon': 'unstoppable', 'Scout Rifle': 'overload', 'Trace Rifle': 'overload'}
            
def generateSimplifiedWeapons(weaponData, destiny):
    simplifiedWeapons=list()
    for weapon in weaponData:
        name = weapon["displayProperties"]["name"]
        type = weapon["itemTypeDisplayName"]
        ammoType = ammoTypes.get(weapon["equippingBlock"]["ammoType"])
        element = damageTypes.get(weapon["defaultDamageType"])
        rarity = weapon["inventory"]["tierTypeName"]
        champion = seasonalChampionMods.get(type, "empty")
        simplifiedWeapons.append(destinyweapon.DestinyWeapon(name, type, ammoType, element, champion, rarity))
    return simplifiedWeapons

def main():
    window()

main()
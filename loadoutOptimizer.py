import pydest
import asyncio
import playerVault
import destinyweapon
from tkinter import *
from tkinter import ttk
import tkinter as tk
import webbrowser

#function for making gui window
def window(pv):
    root = tk.Tk()
    frame = ttk.Frame(root, padding=20)
    frame.grid()
    ttk.Label(frame, text="Destiny 2 Lost Sector Loadout Recommender").grid(row=0,column=0)
    quitButton = ttk.Button(frame, text="QUIT", command=root.destroy).grid(row=0,column=2,ipadx=0,ipady=0)

    #authorization button
    ttk.Label(frame, text="Authorize Bungie Account").grid(row=2,column=0)
    ttk.Button(frame,text="Authorize", command=openAuthPortal).grid(row=3,column=0)

    #date entry for lost sector
    ttk.Label(frame, text="Enter Date:").grid(row=4, column=0)
    dateEntry = ttk.Entry(frame)
    dateEntry.grid(row=4, column=1)
    ttk.Button(frame, text="submit",command=lambda:pv.setDate(dateEntry.get())).grid(row=4,column=2)
    dateErrorMsg = ttk.Label(frame, text="Use xx/xx/xxxx format")
    dateErrorMsg.grid(row=4, column=3)
    #TODO: implement error catching for incorrectly formatted dates, or a different date input system, finish authentication process

    #generate loadout button
    primaryWepLabel = ttk.Label(frame, text="")
    primaryWepLabel.grid(row=9, column=0)
    specialWepLabel = ttk.Label(frame, text="")
    specialWepLabel.grid(row=9, column=1)
    heavyWepLabel = ttk.Label(frame, text="")
    heavyWepLabel.grid(row=9, column=2)
    
    ttk.Button(frame, text="Generate Loadout!", command=lambda: displayLoadout(dateErrorMsg, primaryWepLabel, specialWepLabel, heavyWepLabel, pv)).grid(row=8,column=1)

    #loadout section
    ttk.Label(frame, text="-- Recommended Loadout --").grid(row=7, column=1, ipadx=10,ipady=10)


    root.mainloop()

def openAuthPortal():
    webbrowser.open_new_tab("https://www.bungie.net/en/oauth/authorize")

def displayLoadout(errorMsg, label1, label2, label3, pv):
    errorMsg.update()
    if(pv.getDate() == ""):
        errorMsg.config(text="Please enter a date",foreground="red")
        errorMsg.update()
        return
    else: errorMsg.config(text="")
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
    

damageTypes = {1:'kinetic', 2:'arc', 3:'solar', 4:'void', 6:'stasis', 7:'strand'}
ammoTypes = {1: 'primary', 2: 'special', 3: 'heavy'}
platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}
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

async def main():
    destiny = pydest.Pydest('f6777de733f847a5a7c8ab50d357d399') #create object to access api using api key

    platform = platforms.get('PC')
    username = "Salsasp#2330"
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
    pv = playerVault.Vault(vaultData, simplifiedWeapons)
    window(pv)

    await destiny.close()
    

main()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
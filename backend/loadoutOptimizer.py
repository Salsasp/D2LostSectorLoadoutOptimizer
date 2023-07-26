import pydest
import asyncio
import playerVault
import destinyweapon
import LostSector
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


def window(): #function to handle application gui
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(0, 0, 500, 500)
    win.setWindowTitle("Destiny 2 Lost Sector Loadout Suggestor")
    titleLabel = QtWidgets.QLabel(win)
    titleLabel.setText("Destiny 2 Lost Sector Loadout Suggestor")
    titleLabel.move((int)((win.width()/2)-titleLabel.width()/2), 0) #create title centered at top of screen

    win.show()
    sys.exit(app.exec_())

damageTypes = {1:'kinetic', 2:'arc', 3:'solar', 4:'void', 6:'stasis', 7:'strand'}
ammoTypes = {1: 'primary', 2: 'special', 3: 'heavy'}
platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}
seasonalChampionMods = {'Auto Rifle': 'barrier', 'Glaive': 'unstoppable', 'Hand Cannon': 'unstoppable', 'Scout Rifle': 'overload', 'Trace Rifle': 'overload'}
mainURL = "https://www.bungie.net/Platform/Destiny2/"
authorizationURL = "https://www.bungie.net/en/OAuth/Authorize" 
tokenURL = "https://www.bungie.net/Platform/App/OAuth/token/" 

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

    vaultData = await destiny.api._get_request(mainURL+str(platform)+"/Profile/"+str(userResponse['Response'][0]['membershipId'])+"/?components=102")
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
    await destiny.close()
    pv = playerVault.Vault(vaultData, simplifiedWeapons)
    window()

    
    

main()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
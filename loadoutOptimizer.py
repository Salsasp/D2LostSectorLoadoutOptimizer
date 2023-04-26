import pydest
import asyncio
import playerVault
import copy

class LostSector:
    def __init__(self, day_of_week, date, name, reward, location, shields, champions, surge):
        self.day_of_week = day_of_week
        self.date = date
        self.name = name
        self.reward = reward
        self.location = location
        self.shields = shields
        self.champions = champions
        self.surge = surge
    def display(self):
        print("Lost Sector: " + self.name + ", " + self.day_of_week + " " + self.date + ", " + self.location\
        + ", " + self.reward + ", ", end='') 
        for element in self.shields:
            print(element + ", ", end='')
        for champion in self.champions:
            print(champion + ", ", end='')
        print(self.surge + '\n')

def initializeSeasonalLostSectors():
    date, champions, shields, seasonalSectors = [], [], [], []
    day_of_week, name, reward, location, surge = "", "", "", "", ""
    file = open('defiance_LS.txt', 'r')
    while file:
        line = file.readline()
        if(line == '\n'):
            continue
        if(not line): 
            file.close()
            break
        splitLine = line.split()
        day_of_week = splitLine[0]
        date = splitLine[1]
        name = splitLine[2]
        location = splitLine[3]
        surge = splitLine[4]
        line = file.readline()
        splitLine = line.split()
        for element in splitLine:
            shields.append(element)
        champions.append(file.readline().strip())
        champions.append(file.readline().strip())
        reward = file.readline().strip()
        seasonalSectors.append(LostSector(day_of_week, date, name, reward, location, shields, champions, surge))
        shields = []
        champions = []
    return seasonalSectors
            

async def generateWeaponTags(weaponData, destiny):
    #TODO: create a map of weapons with keys corresponding to weapon atributes (eg. energy type, weapon type, etc.)
    dehashedWeaponCategories = []
    categories = []
    for weapon in weaponData:
        for element in weapon['itemCategoryHashes']:
            categories.append(await destiny.decode_hash(element, 'DestinyItemCategoryDefinition'))
        dehashedWeaponCategories.append(copy.copy(categories))
        categories = []
    return dehashedWeaponCategories #this list contains what type of weapon, what slot, (hopefully energy type too), and I also hope to find other properties as well

platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}

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
       decodedWeapons.append(dehashedItem) 
    weaponTags = await generateWeaponTags(decodedWeapons, destiny)
   # currVault = playerVault.Vault(decodedWeapons, destiny)
    #itemCategory = await destiny.decode_hash(decodedWeapons[0]['itemCategoryHashes'][0], 'DestinyItemCategoryDefinition')

    await destiny.close()
    

main()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
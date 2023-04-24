import pydest
import asyncio
#TODO: add code to dehash all weapons in player vault, add them to a list, and use some sort of data structure(undetermined) to sort weapons based on their different attributes
class Vault: 
    def __init__(self, playerVaultData):
        self.itemData = playerVaultData
        self.weaponTags = self.generateWeaponTags(playerVaultData)

    def decodeWeaponHashes(weaponList):
        pass #change later

    def generateWeaponTags(weapons):
        pass #TODO: create a map of weapons with keys corresponding to weapon atributes (eg. energy type, weapon type, etc.)
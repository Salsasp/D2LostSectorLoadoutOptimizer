import pydest
import asyncio
#TODO: add code to dehash all weapons in player vault, add them to a list, and use some sort of data structure(undetermined) to sort weapons based on their different attributes
class Vault: 
    def __init__(self, playerVaultData, weaponTags, destiny):
        self.weaponData = playerVaultData
        self.destiny = destiny
        self.weaponTags = weaponTags

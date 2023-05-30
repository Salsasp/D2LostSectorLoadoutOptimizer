import pydest
import asyncio

class DestinyWeapon:
    def __init__(self, name, type, ammoType, element, champion, rarity):
        self.name = name
        self.type = type
        self.ammoType = ammoType
        self.element = element
        self.champion = champion
        self.rarity = rarity

    def getName(self):
        return self.name
    def getType(self):
        return self.type
    def getAmmoType(self):
        return self.ammoType
    def getElement(self):
        return self.element
    def getChampion(self):
        return self.champion
    def getRarity(self):
        return self.rarity
    def getWeaponScore(self):
        return self.weaponScore
    def getWeaponScoreByWeapon(weapon):
        return weapon.getWeaponScore() #probably a better way to do this but I need it for sort key
    
    def setWeaponScore(self,value): #store the reccomendation score for the weapon
        self.weaponScore = value


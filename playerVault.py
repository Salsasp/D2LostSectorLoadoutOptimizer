import pydest
import asyncio
import LostSector
import destinyweapon
#ULTRA TODO: rewrite this program in javascript in order to implement it as a website, which will allow for easy oauth
class Vault: 

    def __init__(self, playerVaultData, simplifiedWeapons):
        self.weaponData = playerVaultData
        self.simplifiedWeapons = simplifiedWeapons
        self.recPrimary = ""
        self.recSpecial = ""
        self.recHeavy = ""
        self.date = ""
        print()

    def processWeapons(self): #function to allow recommendations to be generated on command, rather than in constructor
        self.generateWeaponScores(self.simplifiedWeapons)
        weaponsByScore = sorted(self.simplifiedWeapons, key = lambda x: destinyweapon.DestinyWeapon.getWeaponScoreByWeapon(x), reverse=True)
        generateLoadout(self, weaponsByScore)
    def getRecPrimary(self):
        return self.recPrimary
    def getRecSpecial(self):
        return self.recSpecial 
    def getRecHeavy(self):
        return self.recHeavy
    def setDate(self, date): #set date of lost sector for rec generation
        self.date = date
    def getDate(self):
        return self.date

    def sortWeaponsByAttributes(self, simplifiedWeapons): #currently useless function
        arc = []; solar = []; void = [] 
        barrier = []; unstoppable = []; overload = []
        legendary = []; exotic = []
        primary = []; special = []; heavy = []
        hand_cannons = []; scout_rifles = []; auto_rifles = []; pulse_rifles = []; sidearms = []; submachine_guns = []; combat_bows = []
        fusion_rifles = []; shotguns = []; sniper_rifles = []; trace_rifles = []; special_gl = []
        rocket_launchers = []; linear_fusion_rifles = []; swords = []; heavy_gl = []; machine_guns = []

        for weapon in simplifiedWeapons:
            #energy
            if weapon.getElement() == "arc":
                arc.append(weapon)
            if weapon.getElement() == "solar":
                solar.append(weapon)
            if weapon.getElement() == "void":
                void.append(weapon)
       
            #champion
            if weapon.getChampion() == "barrier":
                barrier.append(weapon)
            if weapon.getChampion() == "unstoppable":
                unstoppable.append(weapon)
            if weapon.getChampion() == "overload":
                overload.append(weapon)
            
            #rarity
            if weapon.getRarity() == "legendary":
                legendary.append(weapon)
            if weapon.getRarity() == "exotic":
                exotic.append(weapon)

            #ammo type
            if weapon.getAmmoType() == "primary":
                primary.append(weapon)
            if weapon.getAmmoType() == "special":
                special.append(weapon)
            if weapon.getAmmoType() == "heavy":
                heavy.append(weapon)

            #weapon type
            if weapon.getType() == "Hand Cannon":
                hand_cannons.append(weapon)
            if weapon.getType() == "Scout Rifle":
                scout_rifles.append(weapon)
            if weapon.getType() == "Auto Rifle":
                auto_rifles.append(weapon)
                #TODO: finish this

        self.elements = {"arc": arc, "solar": solar, "void": void}

    def generateWeaponScores(self, simplifiedWeapons):
        #use this function to assign a number to each weapon based off of how many favorable modifiers it reaches when comparing
        #its attributes to the daily lost sector champions, surge, etc.
        #surge and overcharge will be weighted more heavily than champ type and shield elements
        #exotics with innate champion perks will be weighted most heavily
        
        #this dict is for storing the intrinsic anti-champion perks of exotics
        exoticIntrinsics = {"Arbalest": "barrier", "Eriana's Vow": "barrier", "The Lament": "barrier", "Revision Zero": "barrier",
                            "Wish-Ender": "barrier", "Divinity": "overload", "Le Monarque": "overload","Thunderlord": "overload", "Bastion": "unstoppable",
                            "Leviathan's Breath": "unstoppable", "Malfeasance": "unstoppable", "Conditional Finality": "overload", "Conditional Finality": "unstoppable"}
        metaExotics = ["Wish-Ender", "Le Monarque", "Gjallarhorn", "Arbalest", "Conditional Finality", "Thunderlord", "Leviathan's Breath"]
        dailySector = LostSector.getSectorByDate(self.date)

        #loop to determine reccomendation score for weapons
        for weapon in simplifiedWeapons:
            currWepScore = 0
            #energy
            if weapon.getElement() in dailySector.getShields(): #!!! fix strings not properly comparing !!!
                currWepScore += 5
            #bonus points if champ and surge match
            if weapon.getChampion() in dailySector.getChamps() and weapon.getElement() == dailySector.getSurge():
                currWepScore += 20
            #champs
            elif weapon.getChampion() in dailySector.getChamps():
                currWepScore += 10
            #surge
            elif weapon.getElement() == dailySector.getSurge():
                currWepScore += 10
            #exotic intrinsics
            if weapon.getRarity() == "Exotic" and exoticIntrinsics.get(weapon.getName()) in dailySector.getChamps():
                currWepScore += 25
                if weapon.getAmmoType() == "special" or weapon.getAmmoType() == "heavy":
                    currWepScore += 10
                if weapon in metaExotics:
                    currWepScore += 25
            if weapon.getRarity() == "Rare":
                currWepScore -= 25
            weapon.setWeaponScore(currWepScore)
            #TODO: overcharge wep -- WIP (need overcharged weapon data for lost sectors)

def generateLoadout(self, scoredWeapons):

    dailySector = LostSector.getSectorByDate(self.date)
    hasExotic, hasPrimary, hasSpecial, hasHeavy, firstSlotOccupied, secondSlotOccupied = False, False, False, False, False, False
    champions = {dailySector.getChamps()[0]: False, dailySector.getChamps()[1]: False}
    #TODO: if both champ slots are true, the 3rd weapon does not need to check
    firstSlotElements = ["kinetic", "stasis", "strand"]
    secondSlotElements = ["arc", "solar", "void"]

    for weapon in scoredWeapons:
        #ensure that there is only one exotic in loadout
        if weapon.getRarity() == "Exotic" and hasExotic == True:
            continue
        if weapon.getRarity() == "Exotic" and hasExotic == False:
            hasExotic = True

        #primary weapon
        if not hasPrimary and weapon.getAmmoType() == "primary" and not champions.get(weapon.getChampion()):
            if firstSlotOccupied and weapon.getElement() in firstSlotElements: #continue loop if weapon slot is full
                continue
            if secondSlotOccupied and weapon.getElement() in secondSlotElements: #continue loop if weapon slot is full
                continue
            if not firstSlotOccupied and weapon.getElement() in firstSlotElements: #check if weapon can fit in first slot
                firstSlotOccupied = True
            if not firstSlotOccupied and weapon.getElement() in secondSlotElements: #check if weapon can fit in second slot
                secondSlotOccupied = True
            hasPrimary = True
            if not weapon.getChampion() == "empty":
                champions[weapon.getChampion()] = True
            equippedPrimary = weapon.getName()

        #special weapon
        if not hasSpecial and weapon.getAmmoType() == "special" and not champions.get(weapon.getChampion()):
            if firstSlotOccupied and weapon.getElement() in firstSlotElements: #continue loop if weapon slot is full
                continue
            if secondSlotOccupied and weapon.getElement() in secondSlotElements:
                continue
            if not firstSlotOccupied and weapon.getElement() in firstSlotElements: #check if weapon can fit in first slot
                firstSlotOccupied = True
            if not firstSlotOccupied and weapon.getElement() in secondSlotElements: #check if weapon can fit in second slot
                secondSlotOccupied = True
            hasSpecial = True
            if not weapon.getChampion() == "empty":
                champions[weapon.getChampion()] = True
            equippedSpecial = weapon.getName()

        #heavy weapon
        if not hasHeavy and weapon.getAmmoType() == "heavy" and not champions.get(weapon.getChampion()):
            hasHeavy = True
            if not weapon.getChampion() == "empty":
                champions[weapon.getChampion()] = True
            equippedHeavy = weapon.getName()
        if hasPrimary and hasSpecial and hasHeavy:
            break
    
    self.recPrimary = equippedPrimary
    self.recSpecial = equippedSpecial
    self.recHeavy = equippedHeavy
    print("Primary: " + equippedPrimary)
    print("Special: " + equippedSpecial)
    print("Heavy: " + equippedHeavy)
    

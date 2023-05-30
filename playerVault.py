import pydest
import asyncio
import LostSector
#TODO: add code to dehash all weapons in player vault, add them to a list, and use some sort of data structure(undetermined) to sort weapons based on their different attributes
class Vault: 

    def __init__(self, playerVaultData, simplifiedWeapons):
        self.weaponData = playerVaultData
        self.simplifiedWeapons = simplifiedWeapons
        self.generateWeaponScores(simplifiedWeapons)

    def sortWeaponsByAttributes(self, simplifiedWeapons):
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
                            "Wish-Ender": "barrier", "Divinity": "overload", "Le Monarque": "overload", "Ruinous Effigy": "overload",
                            "Thunderlord": "overload", "Wavesplitter": "overload", "Bastion": "unstoppable", "Devil's Ruin": "unstoppable",
                            "Leviathan's Breath": "unstoppable", "Malfeasance": "unstoppable",}
        dailySector = LostSector.initializeSeasonalLostSectors()[0] #this is VERY temporary for debugging
        for weapon in simplifiedWeapons:
            currWepScore = 0
            #energy
            if weapon.getElement() in dailySector.getShields(): #!!! fix strings not properly comparing !!!
                currWepScore += 3
            #champs
            if weapon.getChampion() in dailySector.getChamps():
                currWepScore += 10
            #surge
            if weapon.getElement() == dailySector.getSurge():
                currWepScore += 15
            #exotic intrinsics
            if weapon.getRarity() == "exotic" and exoticIntrinsics.get(weapon.getName()) in dailySector.getChamps():
                currWepScore += 20

            #overcharge wep -- WIP (need overcharged weapon data for lost sectors)
            

import json

class PlayerHelper():

    def __init__(self):
        self.players = self.loadPlayers()


    def loadPlayers(self):
        try:
            f = open(f"./GoblinData/stats.json", "r")
            stats = json.load(f)
            f.close()
        except:
            stats = self.__initStats__()

        return stats

    def savePlayers(self):
        f = open(f"./GoblinData/stats.json" "w")
        f.write(json.dump(self.stats))
        f.close()

    def __initStats__(self):
        stats = {}
        for i in range(1, len(self.goblins)):
            attrs = attribute_list_to_map(self.goblins[i]['attributes'])

            attack = 0
            defence = 0

            if(attrs["Body"] == "Skinny"):
                strength = 3
                dexterity = 9
                constitution = 3
                wisdom = 6
                luck = 5
            elif(attrs["Body"] == "Strong"):
                strength = 7
                dexterity = 4
                constitution = 7
                wisdom = 4
                luck = 5
            else: # average
                strength = 5
                dexterity = 7
                constitution = 5
                wisdom = 5
                luck = 5

            if(attrs["Head"] == "Gurd"):
                dexterity += 1
            elif(attrs["Head"] == "Wort"):
                constitution += 1
            elif(attrs["Head"] == "Chad"):
                strength += 1
                wisdom -= 1
            elif(attrs["Head"] == "Chadder"):
                strength += 1
                constitution += 1
                wisdom -= 1
                luck += 1
            elif(attrs["Head"] == "Coomer"):
                luck -= 1
                constitution += 1
            elif(attrs["Head"] == "Tervis"):
                wisdom -= 1
                dexterity += 2
            elif(attrs["Head"] == "Goofus"):
                wisdom -= 2
                strength += 1
                luck += 1
            elif(attrs["Head"] == "Roy"):
                luck += 1
            elif(attrs["Head"] == "Gramps"):
                wisdom += 2
                constitution -= 2
                luck += 1
                dexterity -= 1
            elif(attrs["Head"] == "Dungo"):
                luck -= 2
                constitution += 1
                wisdom -= 1
                dexterity += 1
            elif(attrs["Head"] == "Onk"):
                strength += 1
            elif(attrs["Head"] == "ChinChin"):
                constitution += 1
            elif(attrs["Head"] == "Dobby"):
                constitution += 1
                dexterity += 1
                strength -= 1
            elif(attrs["Head"] == "Slash"):
                constitution += 1
                luck += 1
            elif(attrs["Head"] == "Dropped As A Baby"):
                wisdom -= 2
                luck += 2

            if(attrs["Skin"] == "Tan, Dirty And Sweaty"):
                constitution -= 1
                strength += 2
            elif(attrs["Skin"] == "Purple, Bloody"):
                constitution += 1
            elif(attrs["Skin"] == "Red, Greasy"):
                dexterity += 1
            elif(attrs["Skin"] == "Green and Brown"):
                luck += 2
                constitution -= 1
            elif(attrs["Skin"] == "Green, Bloody"):
                constitution += 1
            elif(attrs["Skin"] == "Yellow, Greasy"):
                strength += 1
                dexterity += 1
            elif(attrs["Skin"] == "White, Bloody"):
                constitution += 1
                wisdom += 1
            elif(attrs["Skin"] == "Blood Soaked"):
                constitution += 2
                luck += 1

            armorquality = 0
            if(attrs["Armor Material"] == "Hammered Copper"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Hammered Copper, Dirty"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Hammered Bronze"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Hammered Bronze, Bloody"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Hammered Iron"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Hammered Iron, Rusty"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Polished Steel"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Polished Steel, Painted"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Mithril"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Mithril, Dirty"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Blood Steel"):
                armorquality = 0
            elif(attrs["Armor Material"] == "Enchanted Mithril"):
                armorquality = 0

            armoramount = 0
            if(attrs["Chest Armor"] == "Breast Plate"):
                armoramount += 1
            elif(attrs["Chest Armor"] == "Spiked Breast Plate"):
                armoramount += 2

            if(attrs["Upper Arm Armor"] == "Rerebraces"):
                armoramount += 1
            elif(attrs["Upper Arm Armor"] == "Spiked Rerebraces"):
                attack += 1
                armoramount += 1

            if(attrs["Lower Arm Armor"] == "Vambraces"):
                armoramount += 1
            elif(attrs["Lower Arm Armor"] == "Spiked Vambraces"):
                attack += 1
                armoramount += 1

            if(attrs["Upper Leg Armor"] == "Cuisses"):
                armoramount += 1
            elif(attrs["Upper Leg Armor"] == "Spiked Cuisses"):
                attack += 1
                armoramount += 1

            if(attrs["Lower Leg Armor"] == "Greaves"):
                armoramount += 1

            if(attrs["Shirt Material"] == "Mesh"):
                dexterity += 1
            elif(attrs["Shirt Material"] == "Bronze Chainmail"):
                if(attrs["Shirt"] == "Long Sleeve"):
                    armoramount += 1
                elif(attrs["Shirt"] == "Short Sleeve"):
                    armoramount += 0.75
                elif(attrs["Shirt"] == "Tanktop"):
                    armoramount += 0.5
            elif(attrs["Shirt Material"] == "Steel Chainmail" or attrs["Shirt Material"] == "Steel Chainmail, Rusty"):
                if(attrs["Shirt"] == "Long Sleeve"):
                    armoramount += 1.5
                elif(attrs["Shirt"] == "Short Sleeve"):
                    armoramount += 1.25
                elif(attrs["Shirt"] == "Tanktop"):
                    armoramount += 1



            weaponquality = 0
            if(attrs["Weapon Material"] == "Hammered Copper"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Hammered Copper, Dirty"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Hammered Bronze"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Hammered Bronze, Bloody"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Hammered Iron"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Hammered Iron, Rusty"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Polished Steel"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Polished Steel, Painted"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Mithril"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Mithril, Dirty"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Blood Steel"):
                weaponquality = 0
            elif(attrs["Weapon Material"] == "Enchanted Mithril"):
                weaponquality = 0

            if(attrs["Weapon"] == "Knife"):
                pass
            elif(attrs["Weapon"] == "Cleaver"):
                pass
            elif(attrs["Weapon"] == "Sickle"):
                pass
            elif(attrs["Weapon"] == "Dagger 1"):
                pass
            elif(attrs["Weapon"] == "Dagger 2"):
                pass
            elif(attrs["Weapon"] == "Sword 1"):
                pass
            elif(attrs["Weapon"] == "Sword 2"):
                pass
            elif(attrs["Weapon"] == "Mace 1"):
                pass
            elif(attrs["Weapon"] == "Mace 2"):
                pass
            elif(attrs["Weapon"] == "Axe 1"):
                pass
            elif(attrs["Weapon"] == "Axe 2"):
                pass

            stats[i] = {
                "Attack": attack,
                "Defence": defence,
                "Strength": strength,
                "Dexterity": dexterity,
                "Constitution": constitution,
                "Wisdom": wisdom,
                "Luck": luck,
                "Experience": 0
            }
        return stats

    def getNumGoblins(self):
        return len(self.goblins)

def attribute_list_to_map(list):
    map = {}
    for i in list:
        map[i['trait_type']] = i['value']
    return map

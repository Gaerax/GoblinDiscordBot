import json
import aiohttp
import time

async def getAddressGoblins(address):
    async with aiohttp.ClientSession() as session:
        headers = {'x-auth-id': 'tkn1qqqkvqgzjfrsnrgz9vzs426texw703kkv065zuckvqgzjfrsjqqq2e48d0',
                   'coin': 'xch',
                   'version': "1.0"
        }
        async with session.get(f"https://api2.spacescan.io/api/nft/balance/{address}", headers=headers) as request:
            if request.status == 200:
                data = await request.json()
                goblins = []
                print(len(data["tokens"]))
                for i, token in enumerate(data["tokens"]):
                    if "Grinning Goblins" in token['nft_name']:
                        num = int(token['nft_name'].split('#')[1])
                        stats = getGoblinStats(num)
                        emojis = ""
                        if stats["Faction"] == "New King":
                            emojis += "🟢"
                        elif stats["Faction"] == "Old King":
                            emojis += "🔴"
                        elif stats["Faction"] == "Mage Supremacy":
                            emojis += "🔵"
                        else:
                            emojis += "🟠"

                        if stats["Rank"] == "Warrior":
                            emojis += "🔪"
                        elif stats["Rank"] == "Lieutenant":
                            emojis += "🗡️"
                        elif stats["Rank"] == "Captian":
                            emojis += "⚔️"
                        elif stats["Rank"] == "Mage":
                            emojis += "🔮"
                        elif stats["Rank"] == "Lord":
                            emojis += "🛡️"
                        elif stats["Rank"] == "King":
                            emojis += "👑"

                        if "Uncommon" in stats["Description"]:
                            emojis += "🔹"
                        elif "Super Rare" in stats["Description"]:
                            emojis += "💎"
                        elif "Rare" in stats["Description"]:
                            emojis += "💠"

                        goblins.append({"name": token['nft_name'], "id": token['inner_mod'], "emojis": emojis})
                return goblins
            else:
                return None

def getGoblinData(goblin):
    f = open(f"./GoblinData/metadata/{goblin}.json", "r")
    data = json.load(f)
    f.close()
    return data


def getGoblinStats(goblin):
    try:
        f = open(f"./GoblinData/stats/{goblin}.json", "r")
        stats = json.load(f)
        f.close()
    except:
        stats = calculateStats(goblin, True)
        updateStats(goblin, stats)

    return stats


def updateStats(goblin, stats):
    stats = calculateStats(goblin, False, oldstats=stats)
    f = open(f"./GoblinData/stats/{goblin}.json", "w")
    json.dump(stats, f, indent=4)
    f.close()


def calculateStats(goblin, resetEXP, oldstats={}):
    data = getGoblinData(goblin)
    attrs = attribute_list_to_map(data['attributes'])
    stats = {}
    if resetEXP:
        stats["Level"] = 1
        stats["Experience"] = 0
    else:
        if oldstats["Experience"] > 100*oldstats["Level"]:
            stats["Level"] = oldstats["Level"] + 1
            stats["Experience"] = oldstats["Experience"]%(100*oldstats["Level"])
        else:
            stats["Level"] = oldstats["Level"]
            stats["Experience"] = oldstats["Experience"]

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
    elif(attrs["Body"] == "Average"):
        strength = 5
        dexterity = 7
        constitution = 5
        wisdom = 5
        luck = 5
    elif(attrs["Body"] == "Old"):
        strength = 4
        dexterity = 3
        constitution = 4
        wisdom = 9
        luck = 7
    elif(attrs["Body"] == "Giant"):
        strength = 9
        dexterity = 3
        constitution = 8
        wisdom = 4
        luck = 4
    elif(attrs["Body"] == "Fat"):
        strength = 8
        dexterity = 3
        constitution = 10
        wisdom = 5
        luck = 7
    elif(attrs["Body"] == "Baby"):
        strength = 0
        dexterity = 0
        constitution = 0
        wisdom = 0
        luck = 10

    if(attrs["Rank"] == "Lieutenant"):
        strength += 1
        dexterity += 1
        constitution += 1
        wisdom += 1
        luck += 1
    elif(attrs["Rank"] == "Captain"):
        strength += 2
        dexterity += 2
        constitution += 2
        wisdom += 2
        luck += 2
    elif(attrs["Rank"] == "Mage"):
        strength += 1
        dexterity += 1
        constitution += 1
        wisdom += 4
        luck += 4
    elif(attrs["Rank"] == "Lord"):
        strength += 3
        dexterity += 3
        constitution += 3
        wisdom += 3
        luck += 3


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
    elif(attrs["Head"] == "Clyrm the Bold"):
        strength += 3
        constitution += 3
        dexterity += 2
        wisdom += 3
        luck += 4
    elif(attrs["Head"] == "Ealluld the Advisor"):
        strength += 3
        constitution += 1
        dexterity += 1
        wisdom += 3
        luck += 3
    elif(attrs["Head"] == "Uzol the Butcher"):
        strength += 5
        constitution += 5
        dexterity += 5
        wisdom += 1
        luck += 2
    elif(attrs["Head"] == "Lil Zunk"):
        strength += 4
        constitution += 5
        dexterity += 5
        wisdom -= 1
        luck += 1
    elif(attrs["Head"] == "Utnar Gold-Fang"):
        strength += 3
        constitution += 4
        dexterity += 4
        wisdom -= 1
        luck += 1
    elif(attrs["Head"] == "Rakt Bloodborn"):
        strength += 2
        constitution += 5
        dexterity += 3
        wisdom -= 1
        luck += 1
    elif(attrs["Head"] == "Wriaq the Defiler"):
        strength += 3
        constitution += 3
        dexterity += 4
        wisdom += 3
        luck += 3
    elif(attrs["Head"] == "Kark the Damned"):
        strength += 3
        constitution += 1
        dexterity += 6
        wisdom += 4
        luck += 5
    elif(attrs["Head"] == "Clyg Flame Lover"):
        strength += 4
        constitution += 6
        dexterity += 5
        wisdom += 1
        luck += 1
    elif(attrs["Head"] == "Frasniel the Wise"):
        strength += 3
        constitution += 1
        dexterity += 1
        wisdom += 3
        luck += 3
    elif(attrs["Head"] == "Drumme the Glutton"):
        strength += 3
        constitution += 3
        dexterity += 1
        wisdom += 3
        luck += 3
    elif(attrs["Head"] == "Craght The Newborn"):
        pass

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

    armorprotection = 0
    armorweight = 0
    if(attrs["Armor Material"] == "Hammered Copper"):
        armorprotection = 0.4
        armorweight = 1
    elif(attrs["Armor Material"] == "Hammered Copper, Dirty"):
        armorprotection = 0.4
        armorweight = 1
    elif(attrs["Armor Material"] == "Hammered Bronze"):
        armorprotection = 0.5
        armorweight = 0.9
    elif(attrs["Armor Material"] == "Hammered Bronze, Bloody"):
        armorprotection = 0.5
        armorweight = 0.9
    elif(attrs["Armor Material"] == "Hammered Iron"):
        armorprotection = 0.7
        armorweight = 0.8
    elif(attrs["Armor Material"] == "Hammered Iron, Rusty"):
        armorprotection = 0.7
        armorweight = 0.8
    elif(attrs["Armor Material"] == "Polished Steel"):
        armorprotection = 0.9
        armorweight = 0.7
    elif(attrs["Armor Material"] == "Polished Steel, Painted"):
        armorprotection = 0.9
        armorweight = 0.7
    elif(attrs["Armor Material"] == "Mithril"):
        armorprotection = .9
        armorweight = 0.5
    elif(attrs["Armor Material"] == "Mithril, Dirty"):
        armorprotection = 0.9
        armorweight = 0.5
    elif(attrs["Armor Material"] == "Blood Steel"):
        armorprotection = 1
        armorweight = 0.5
    elif(attrs["Armor Material"] == "Enchanted Mithril"):
        armorprotection = 1
        armorweight = 0.3
    elif(attrs["Armor Material"] == "Polished Gold"):
        armorprotection = 0.7
        armorweight = 0.7
    elif(attrs["Armor Material"] == "Red Painted Steel"):
        armorprotection = 0.9
        armorweight = 0.7

    armoramount = 0
    if(attrs["Chest Armor"] == "Breast Plate"):
        armoramount += 5
    elif(attrs["Chest Armor"] == "Spiked Breast Plate"):
        armoramount += 6

    if(attrs["Upper Arm Armor"] == "Rerebraces"):
        armoramount += 3
    elif(attrs["Upper Arm Armor"] == "Spiked Rerebraces"):
        armoramount += 3.5
    elif(attrs["Upper Arm Armor"] == "Kings Pauldrons"):
        armoramount += 4

    if(attrs["Lower Arm Armor"] == "Vambraces"):
        armoramount += 2
    elif(attrs["Lower Arm Armor"] == "Spiked Vambraces"):
        armoramount += 2.5
    elif(attrs["Lower Arm Armor"] == "Kings Vambraces"):
        armoramount += 3

    if(attrs["Upper Leg Armor"] == "Cuisses"):
        armoramount += 3
    elif(attrs["Upper Leg Armor"] == "Spiked Cuisses"):
        armoramount += 3.5

    if(attrs["Lower Leg Armor"] == "Greaves"):
        armoramount += 2

    if(attrs["Shirt Material"] == "Mesh"):
        dexterity += 2
    elif(attrs["Shirt Material"] == "Bronze Chainmail"):
        if(attrs["Shirt"] == "Long Sleeve"):
            armoramount += 1
        elif(attrs["Shirt"] == "Short Sleeve"):
            armoramount += 0.85
        elif(attrs["Shirt"] == "Tanktop"):
            armoramount += 0.7
    elif(attrs["Shirt Material"] == "Steel Chainmail" or attrs["Shirt Material"] == "Steel Chainmail, Rusty"):
        if(attrs["Shirt"] == "Long Sleeve"):
            armoramount += 1.5
        elif(attrs["Shirt"] == "Short Sleeve"):
            armoramount += 1.25
        elif(attrs["Shirt"] == "Tanktop"):
            armoramount += 1


    weaponmatquality = 0
    weaponmatweight = 0
    if(attrs["Weapon Material"] == "Hammered Copper"):
        weaponmatquality = 0.5
        weaponmatweight = 1
    elif(attrs["Weapon Material"] == "Hammered Copper, Dirty"):
        weaponmatquality = 0.5
        weaponmatweight = 1
    elif(attrs["Weapon Material"] == "Hammered Bronze"):
        weaponmatquality = 0.6
        weaponmatweight = 0.9
    elif(attrs["Weapon Material"] == "Hammered Bronze, Bloody"):
        weaponmatquality = 0.6
        weaponmatweight = 0.9
    elif(attrs["Weapon Material"] == "Hammered Iron"):
        weaponmatquality = 0.7
        weaponmatweight = 0.8
    elif(attrs["Weapon Material"] == "Hammered Iron, Rusty"):
        weaponmatquality = 0.7
        weaponmatweight = 0.8
    elif(attrs["Weapon Material"] == "Polished Steel"):
        weaponmatquality = 0.9
        weaponmatweight = 0.7
    elif(attrs["Weapon Material"] == "Polished Steel, Painted"):
        weaponmatquality = 0.9
        weaponmatweight = 0.7
    elif(attrs["Weapon Material"] == "Mithril"):
        weaponmatquality = .9
        weaponmatweight = 0.5
    elif(attrs["Weapon Material"] == "Mithril, Dirty"):
        weaponmatquality = 0.9
        weaponmatweight = 0.5
    elif(attrs["Weapon Material"] == "Blood Steel"):
        weaponmatquality = 1
        weaponmatweight = 0.5
    elif(attrs["Weapon Material"] == "Enchanted Mithril"):
        weaponmatquality = 1
        weaponmatweight = 0.3
    elif(attrs["Weapon Material"] == "Wood"):
        weaponmatquality = .7
        weaponmatweight = 0.1
    elif(attrs["Weapon Material"] == "Wood and Crystal"):
        weaponmatquality = 1
        weaponmatweight = 0.2
    elif(attrs["Weapon Material"] == "Polished Gold"):
        weaponmatquality = 0.8
        weaponmatweight = 0.5
    elif(attrs["Weapon Material"] == "Polished Iron"):
        weaponmatquality = 0.8
        weaponmatweight = 0.5


    weapondamage = 0
    weaponweight = 0
    if(attrs["Weapon"] == "Knife"):
        weapondamage = 3
        weaponweight = 1
    elif(attrs["Weapon"] == "Cleaver"):
        weapondamage = 4
        weaponweight = 1.5
    elif(attrs["Weapon"] == "Sickle"):
        weapondamage = 5
        weaponweight = 1
    elif(attrs["Weapon"] == "Dagger 1"):
        weapondamage = 5
        weaponweight = 1.5
    elif(attrs["Weapon"] == "Dagger 2"):
        weapondamage = 6
        weaponweight = 2
    elif(attrs["Weapon"] == "Sword 1"):
        weapondamage = 6
        weaponweight = 3
    elif(attrs["Weapon"] == "Sword 2"):
        weapondamage = 7
        weaponweight = 3.5
    elif(attrs["Weapon"] == "Mace 1"):
        weapondamage = 7
        weaponweight = 9
    elif(attrs["Weapon"] == "Mace 2"):
        weapondamage = 8
        weaponweight = 10
    elif(attrs["Weapon"] == "Axe 1"):
        weapondamage = 9
        weaponweight = 8
    elif(attrs["Weapon"] == "Axe 2"):
        weapondamage = 10
        weaponweight = 8
    elif(attrs["Weapon"] == "Dual Knife"):
        weapondamage = 5
        weaponweight = 2
    elif(attrs["Weapon"] == "Dual Cleaver"):
        weapondamage = 4
        weaponweight = 3
    elif(attrs["Weapon"] == "Dual Sickle"):
        weapondamage = 5
        weaponweight = 2
    elif(attrs["Weapon"] == "Dual Dagger 1"):
        weapondamage = 5
        weaponweight = 3
    elif(attrs["Weapon"] == "Dual Dagger 2"):
        weapondamage = 6
        weaponweight = 4
    elif(attrs["Weapon"] == "Dual Sword 1"):
        weapondamage = 6
        weaponweight = 6
    elif(attrs["Weapon"] == "Dual Sword 2"):
        weapondamage = 7
        weaponweight = 7
    elif(attrs["Weapon"] == "Dual Mace 1"):
        weapondamage = 7
        weaponweight = 18
    elif(attrs["Weapon"] == "Dual Mace 2"):
        weapondamage = 8
        weaponweight = 20
    elif(attrs["Weapon"] == "Dual Axe 1"):
        weapondamage = 9
        weaponweight = 16
    elif(attrs["Weapon"] == "Dual Axe 2"):
        weapondamage = 10
        weaponweight = 16
    elif(attrs["Weapon"] == "Stalf"):
        weapondamage = 10
        weaponweight = 2
    elif(attrs["Weapon"] == "Sword and Shield"):
        weapondamage = 5
        weaponweight = 3
        armoramount += 3
        armorprotection += 0.2
    elif(attrs["Weapon"] == "Giant Cleaver"):
        weapondamage = 6
        weaponweight = 2
    elif(attrs["Weapon"] == "Giant Axe"):
        weapondamage = 15
        weaponweight = 14
    elif(attrs["Weapon"] == "Spear"):
        weapondamage = 8
        weaponweight = 3
    elif(attrs["Weapon"] == "Spear and Shield"):
        weapondamage = 8
        weaponweight = 3
        armoramount += 5
        armorprotection += 0.3
    elif(attrs["Weapon"] == "Dual Barbed Swords"):
        weapondamage = 9
        weaponweight = 5
    elif(attrs["Weapon"] == "Dual Spiked Knuckles"):
        weapondamage = 6
        weaponweight = 1
    elif(attrs["Weapon"] == "Dual Torches"):
        weapondamage = 10
        weaponweight = 7
    elif(attrs["Weapon"] == "Giant Mace"):
        weapondamage = 15
        weaponweight = 14

    weapondamage *= weaponmatquality
    weaponweight *= weaponmatweight

    armorweight = armoramount * armorweight
    armorquality = armoramount * armorprotection


    stats["Name"] = data["name"]
    stats["Description"] = data["description"]
    stats["Rank"] = attrs["Rank"]
    stats["Faction"] = attrs["Faction"]
    stats["Body"] = attrs["Body"]
    if "Last Trained" in oldstats:
        stats["Last Trained"] = oldstats["Last Trained"]
    else:
        stats["Last Trained"] = 0

    basestats = {}
    basestats["Strength"] = strength
    basestats["Dexterity"] = dexterity
    basestats["Constitution"] = constitution
    basestats["Wisdom"] = wisdom
    basestats["Luck"] = luck

    leveladvantage = (stats["Level"]-1)
    battlestats = {}
    battlestats["Attack Damage"] = (leveladvantage*2) + weapondamage + strength
    battlestats["Attack Speed"] = (leveladvantage*2) + 20 - weaponweight + (dexterity - armorweight)
    battlestats["Accuracy"] = (leveladvantage*1) + luck + wisdom + dexterity
    battlestats["Evasion"] = (leveladvantage*2) + dexterity - armorweight + luck + wisdom
    battlestats["Defence"] = (leveladvantage*1) + armorquality
    battlestats["Health"] = (leveladvantage*5) + constitution * 10

    stats["Base Stats"] = basestats
    stats["Battle Stats"] = battlestats

    return stats


def attribute_list_to_map(list):
    map = {}
    for i in list:
        map[i['trait_type']] = i['value']
    return map

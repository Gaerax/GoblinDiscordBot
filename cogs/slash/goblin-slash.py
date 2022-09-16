""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1.1
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, Role, File
from disnake.ext import commands

from helpers import checks
from helpers import goblinhelper
from helpers import chiahelper
from helpers import battle

import aiohttp
import json
import random
import math
import time


def writePlayers(players):
    f = open("players.json", "w")
    json.dump(players, f, indent=4)
    f.close


def readPlayers():
    try:
        f = open("players.json", "r")
        players = json.load(f)
        f.close()
    except:
        print("Read players Failed")
        return {}
    return players


# Here we name the cog and create a new class for the cog.
class Goblin(commands.Cog, name="goblin-slash"):
    def __init__(self, bot):
        self.bot = bot
        self.players = readPlayers()

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="viewusergoblins",
        description="Get a list of all goblins owned by a users",
        options=[
            Option(
                name="user",
                description="The user whose goblins you want to view.",
                type=OptionType.user,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def viewusergoblins(self, interaction: ApplicationCommandInteraction, user: disnake.User):
        player = self.players[str(user.id)]
        goblins = await goblinhelper.getAddressGoblins(player["address"])
        if goblins != None:
            current_embed = disnake.Embed(
                title=f"{user.display_name} has {len(goblins)} Goblins",
                description=f"Goblins",
                color=user.color
            )
            embeds = []
            current_embed = None
            embedNum = 1
            for i, goblin in enumerate(goblins):
                if i % 24 == 0:
                    end = min(24*embedNum, len(goblins))
                    current_embed = disnake.Embed(
                        title=f"{user.display_name} has {len(goblins)} Goblins",
                        description=f"{(embedNum-1)*24+1} -> {end}",
                        color=user.color
                    )
                    embeds.append(current_embed)
                    embedNum += 1
                current_embed.add_field(name=f"{goblin['name']} {goblin['emojis']}", value=f"https://www.spacescan.io/xch/nft/{goblin['id']}")

            for e in embeds:
                await interaction.send(embed=e)
        else:
            embed = disnake.Embed(
                title=f"{user.display_name} has no goblins...",
                description=f"That's pretty sad.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="getaddress",
        description="Get the address of a users goblin army",
        options=[
            Option(
                name="user",
                description="The user whose address you want.",
                type=OptionType.user,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def getaddress(self, interaction: ApplicationCommandInteraction, user: disnake.User) -> None:
        try:
            embed = disnake.Embed(
                title=f"{user.display_name}'s Goblin Army Address",
                description=f"{user}'s address is: " + self.players[str(user.id)]["address"],
                color=user.color
            )
        except:
            embed = disnake.Embed(
                title="Error",
                description=f"{user.display_name} has not set their address.",
                color=user.color
            )
        await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="setaddress",
        description="Set your goblin army xch address",
        options=[
            Option(
                name="address",
                description="The xch address that contains your goblins",
                type=OptionType.string,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def setaddress(self, interaction: ApplicationCommandInteraction, address: str="") -> None:

        for playerID in self.players.keys():
            if str(interaction.author.id) in self.players:
                if playerID != self.players[str(interaction.author.id)]:
                    if self.players[playerID]["address"] == self.players[str(interaction.author.id)]["address"] and (playerID != str(interaction.author.id)):
                        embed = disnake.Embed(
                            title="Address already in use!",
                            description=f"Address {address} is being used by: {str(self.players[playerID]['name'])}. Please notify an Admin if this is your address.",
                            color=0xE02B2B
                        )
                        await interaction.send(embed=embed)
                        return

        justjoined = False
        if str(interaction.author.id) not in self.players:
            justjoined = True
            self.players[str(interaction.author.id)] = {}

        self.players[str(interaction.author.id)]["address"] = address
        self.players[str(interaction.author.id)]["name"] = interaction.author.name

        random.seed(interaction.author.id)
        faction = random.randint(1, 4)
        if faction == 1:
            role = disnake.utils.find(lambda r: r.name == 'Follower of the New King', interaction.channel.guild.roles)
            faction = "New King"
        elif faction == 2:
            role = disnake.utils.find(lambda r: r.name == 'Follower of the Old King', interaction.channel.guild.roles)
            faction = "Old King"
        elif faction == 3:
            role = disnake.utils.find(lambda r: r.name == 'Follower of the Mage Supremacy', interaction.channel.guild.roles)
            faction = "Mage Supremacy"
        else:
            role = disnake.utils.find(lambda r: r.name == 'Follower of the Lords Alliance', interaction.channel.guild.roles)
            faction = "Lords Alliance"

        self.players[str(interaction.author.id)]["faction"] = faction

        writePlayers(self.players)

        await interaction.author.add_roles(role)

        newbie = disnake.utils.find(lambda r: r.name == 'newbie', interaction.channel.guild.roles)
        await interaction.author.remove_roles(newbie)

        embed = disnake.Embed(
            title="Address set",
            description=f"Set address {address} for: {str(interaction.author.display_name)}\n You are part of the {role.name} faction!",
            color=role.color
        )
        await interaction.send(embed=embed)

        if justjoined:
            embed = await chiahelper.sendgold(interaction.author, 100, address, f"100 gold has been set to your address\nThanks for joining!")
            await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="goblindata",
        description="Display a specific goblin and its metadata.",
        options=[
            Option(
                name="number",
                description="The goblin number.",
                type=OptionType.integer,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def goblindata(self, interaction: ApplicationCommandInteraction, number: int) -> None:
        try:
            data = goblinhelper.getGoblinData(number)
            attrs = data['attributes']
            color = 0x000000
            for attr in attrs:
                if attr['trait_type'] == "Faction":
                    if attr["value"] == "New King":
                        role = disnake.utils.find(lambda r: r.name == 'Follower of the New King', interaction.channel.guild.roles)
                    elif attr["value"] == "Old King":
                        role = disnake.utils.find(lambda r: r.name == 'Follower of the Old King', interaction.channel.guild.roles)
                    elif attr["value"] == "Mage Supremacy":
                        role = disnake.utils.find(lambda r: r.name == 'Follower of the Mage Supremacy', interaction.channel.guild.roles)
                    else:
                        role = disnake.utils.find(lambda r: r.name == 'Follower of the Lords Alliance', interaction.channel.guild.roles)
                    color = role.color
                    break

            embed = disnake.Embed(
                title=data["name"],
                description=data["description"],
                color=color
            )
            for attr in attrs:
                if "Piercing" not in attr['trait_type']:
                    embed.add_field(name=attr['trait_type'], value=attr['value'], inline=True)
            embed.set_image(file=File(f"GoblinData/img/{number}.jpg"))
        except Exception as e:
            print(e)
            embed = disnake.Embed(
                title="Error",
                description=f"Goblin not found",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="goblinstats",
        description="Display the combat stats of a specific goblin.",
        options=[
            Option(
                name="number",
                description="The goblin number.",
                type=OptionType.integer,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def goblinstats(self, interaction: ApplicationCommandInteraction, number: int) -> None:
        try:
            stats = goblinhelper.getGoblinStats(number)
            color = 0x000000
            if stats["Faction"] == "New King":
                role = disnake.utils.find(lambda r: r.name == 'Follower of the New King', interaction.channel.guild.roles)
            elif stats["Faction"] == "Old King":
                role = disnake.utils.find(lambda r: r.name == 'Follower of the Old King', interaction.channel.guild.roles)
            elif stats["Faction"] == "Mage Supremacy":
                role = disnake.utils.find(lambda r: r.name == 'Follower of the Mage Supremacy', interaction.channel.guild.roles)
            else:
                role = disnake.utils.find(lambda r: r.name == 'Follower of the Lords Alliance', interaction.channel.guild.roles)
            color = role.color

            embed = disnake.Embed(
                title=stats['Name'],
                description=f"Lvl: {stats['Level']} {stats['Description']} Exp:{stats['Experience']}/{stats['Level']*100}",
                color=color
            )

            embed.add_field(name="Battle Stats", value="Current stats used for battle", inline=False)
            for key in stats["Battle Stats"].keys():
                embed.add_field(name=key, value=stats['Battle Stats'][key], inline=True)

            embed.add_field(name="Base Stats", value="Characters base stats", inline=False)
            for key in stats["Base Stats"].keys():
                embed.add_field(name=key, value=stats['Base Stats'][key], inline=True)

            embed.set_image(file=File(f"GoblinData/img/{number}.jpg"))
        except Exception as e:
            print(e)
            embed = disnake.Embed(
                title="Error",
                description=f"Goblin not found",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="postchallenge",
        description="Post a challenge",
        options=[
            Option(
                name="name",
                description="The name of the challenge",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="description",
                description="Description of the challenge.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="deadline",
                description="When the challenge ends.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="reward",
                description="What the winner of the challenge gets.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="role",
                description="Role color of the challenge",
                type=OptionType.string,
                required=False
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    @checks.is_owner()
    async def postchallenge(self, interaction: ApplicationCommandInteraction, name: str, description: str, deadline: str, reward: str, role: str="") -> None:
        try:
            if role == "new":
                color = 0x57F287
            elif role == "old":
                color = 0xED4245
            elif role == "mages":
                color = 0x3498DB
            elif role == "lords":
                color = 0xE67E22
            else:
                color = 0x000000

            embed = disnake.Embed(
                title=f"{name}",
                color=color
            )
            embed.add_field(name="Description", value=description, inline=False)
            embed.add_field(name="Deadline", value=deadline, inline=True)
            embed.add_field(name="Reward", value=reward, inline=True)
        except Exception as e:
            print(e)
            embed = disnake.Embed(
                title="Error",
                description=f"Error",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)



    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="postsimple",
        description="Simple info post",
        options=[
            Option(
                name="name",
                description="The name of the challenge",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="description",
                description="Description of the challenge.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="fieldname",
                description="Field name.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="fielddesc",
                description="Field description.",
                type=OptionType.string,
                required=False
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    @checks.is_owner()
    async def postsimple(self, interaction: ApplicationCommandInteraction, name: str, description: str="", fieldname: str="", fielddesc: str="") -> None:
        try:
            embed = disnake.Embed(
                title=f"{name}",
                description=f"{description}"
            )
            if fieldname != "":
                embed.add_field(name=fieldname, value=fielddesc, inline=False)
        except Exception as e:
            print(e)
            embed = disnake.Embed(
                title="Error",
                description=f"Error",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="duel1v1",
        description="Propose a 1v1 goblin duel with another user.",
        options=[
            Option(
                name="opponent",
                description="The name of user you are challenging.",
                type=OptionType.user,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def duel1v1(self, interaction: ApplicationCommandInteraction, opponent: disnake.User) -> None:
        useraddress = self.players[str(interaction.author.id)]["address"]
        usergoblins = await goblinhelper.getAddressGoblins(useraddress)
        userGoblinList = []
        if usergoblins != None:
            for g in usergoblins:
                userGoblinList.append(disnake.SelectOption(label=g["name"]))
        opponentaddress = self.players[str(opponent.id)]["address"]
        opponentgoblins = await goblinhelper.getAddressGoblins(opponentaddress)
        opponentGoblinList = []
        if usergoblins != None:
            for g in opponentgoblins:
                opponentGoblinList.append(disnake.SelectOption(label=g["name"]))

        if interaction.channel_id == 1015340771777462353:
            view = battle.DualPostView(interaction, interaction.author, useraddress, userGoblinList, opponent, opponentaddress, opponentGoblinList, True)
        else:
            view = battle.DualPostView(interaction, interaction.author, useraddress, userGoblinList, opponent, opponentaddress, opponentGoblinList, False)

        await interaction.send(view=view)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="traingoblins",
        description="Train all of your goblins."
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def traingoblins(self, interaction: ApplicationCommandInteraction) -> None:
        try:
            useraddress = self.players[str(interaction.author.id)]["address"]
            usergoblins = await goblinhelper.getAddressGoblins(useraddress)
        except:
            usergoblins = []
        updates = []
        goblinlist = []
        if len(usergoblins) >= 1:
            for g in usergoblins:
                stats = goblinhelper.getGoblinStats(g["name"].split("#")[1])
                faction = stats["Faction"]
                print(f"goblin: {faction} user: {self.players[str(interaction.author.id)]['faction']} train?: {faction == self.players[str(interaction.author.id)]['faction']}")
                if faction == self.players[str(interaction.author.id)]["faction"]:
                    goblinlist.append(g["name"].split("#")[1])

            for goblinnum in goblinlist:
                stats = goblinhelper.getGoblinStats(goblinnum)
                now = time.time()
                if stats["Last Trained"] + 86400 < now:
                    gain = random.randint(20, 40)
                    stats["Experience"] += gain
                    updates.append(f"Goblin #{goblinnum} gained {gain}XP!")
                stats["Last Trained"] = time.time()
                goblinhelper.updateStats(goblinnum, stats)

            print(f"len updates: {len(updates)}")
            print(f"len goblinlist: {len(goblinlist)}")
            print(f"len usergoblins: {len(usergoblins)}")
            print(f"updates: {updates}")
            if len(updates) >= 1:
                embed = disnake.Embed(
                    title=f"{interaction.author.display_name} has trained {len(goblinlist)} goblins!",
                    description=f"That's awesome!",
                    color=0xE02B2B
                )
                for update in updates:
                    embed.add_field(name="Goblin Trained!", value=update)
                await interaction.send(embed=embed)

                embed = await chiahelper.sendgold(interaction.author, 10*len(updates), useraddress, f"{10*len(updates)} gold has been set to your address\nKeep training every day to earn more!")
                await interaction.send(embed=embed)
            else:
                if len(goblinlist) >= 1:
                    embed = disnake.Embed(
                        title=f"{interaction.author.display_name}'s goblins are tired...",
                        description=f"Goblins can only be trained every 24 hours.",
                        color=0xE02B2B
                    )
                    await interaction.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title=f"{interaction.author.display_name} has no goblins to train...",
                        description=f"You can only train goblins that part of your faction.",
                        color=0xE02B2B
                    )
                    await interaction.send(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"{interaction.author.display_name} has no goblins to train...",
                description=f"That's pretty sad. (You can only train goblins belonging to your own faction)",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="rewarduser",
        description="**Admin only** Send a user some gold.",
        options=[
            Option(
                name="user",
                description="The user to reward.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="amount",
                description="Amount of gold",
                type=OptionType.integer,
                required=True
            ),
            Option(
                name="message",
                description="message to user",
                type=OptionType.string,
                required=False
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    @checks.is_owner()
    async def rewarduser(self, interaction: ApplicationCommandInteraction, user: disnake.User, amount: int, message: str="Keep it up!") -> None:
        useraddress = self.players[str(user.id)]["address"]
        usergoblins = await goblinhelper.getAddressGoblins(useraddress)
        userGoblinList = []

        embed = await chiahelper.sendgold(user, amount, useraddress, message)
        await interaction.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Goblin(bot))

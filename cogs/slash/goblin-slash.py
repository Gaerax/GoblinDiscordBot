""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1.1
"""

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import checks

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.config import load_config_cli, load_config
from chia.util.ints import uint16
from chia.util.bech32m import decode_puzzle_hash

import aiohttp
import json

def writeAddresses(addresses):
    f = open("addresses.json", "w")
    f.write(json.dumps(addresses))
    f.close

def readAddresses():
    try:
        f = open("addresses.json", "r")
        addresses = json.load(f)
        f.close()
    except:
        print("Read Addresses Failed")
        return {}
    return addresses

# Here we name the cog and create a new class for the cog.
class Goblin(commands.Cog, name="goblin-slash"):
    def __init__(self, bot):
        self.bot = bot
        self.addresses = readAddresses()
        self.config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        self.full_node_rpc_port = self.config['full_node']['rpc_port']


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="goblinstats",
        description="Gets the stats of a goblin by number",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def goblinstats(self, interaction: ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Address set",
            description="Set address: ",
            color=0xE02B2B
        )
        await interaction.send(embed=embed)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="mygoblins",
        description="Get a list of your goblins",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def mygoblins(self, interaction: ApplicationCommandInteraction):
        address = self.addresses[str(interaction.author.id)]
        async with aiohttp.ClientSession() as session:
            headers = {'x-auth-id': 'tkn1qqqkvqgzjfrsnrgz9vzs426texw703kkv065zuckvqgzjfrsjqqq2e48d0'}
            async with session.get("https://api2.spacescan.io/api/nft/balance/" + address, headers=headers) as request:
                print(f"status: {request.status} {request.headers}")
                if request.status == 200:
                    data = await request.json()  # For some reason the returned content is of type JavaScript
                    print(data)
                    list = ""
                    for token in data['tokens']:
                        list += token['nft_name'] + "\n"
                    embed = disnake.Embed(
                        title="Goblins",
                        description=f"You have {len(data['tokens'])} Goblins!\n {list}",
                        color=0x9C84EF
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )

        await interaction.send(embed=embed)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="myaddress",
        description="Get the address of your goblin army",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def myaddress(self, interaction: ApplicationCommandInteraction) -> None:
        try:
            embed = disnake.Embed(
                title="Your Goblin Army Address",
                description="Your address is: " + self.addresses[str(interaction.author.id)],
                color=0xE02B2B
            )
        except:
            embed = disnake.Embed(
                title="Error",
                description="You have not set your address yet.",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="findaddress",
        description="Get the address of another users goblin army",
        options=[
            Option(
                name="user",
                description="The xch address that contains your goblins",
                type=OptionType.user,
                required=True
            )]
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def findaddress(self, interaction: ApplicationCommandInteraction, user: disnake.User) -> None:
        try:
            embed = disnake.Embed(
                title=f"{user}'s Goblin Army Address",
                description=f"{user}'s address is: " + self.addresses[str(user.id)],
                color=0xE02B2B
            )
        except:
            embed = disnake.Embed(
                title="Error",
                description=f"{user} has not set their address.",
                color=0xE02B2B
            )
        await interaction.send(embed=embed)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="setgoblinaddress",
        description="set your goblin army xch address",
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
    async def setgoblinaddress(self, interaction: ApplicationCommandInteraction, address: str="") -> None:

        self.addresses[str(interaction.author.id)] = address
        writeAddresses(self.addresses)
        embed = disnake.Embed(
            title="Address set",
            description="Set address " + address + " for: " + str(interaction.author),
            color=0xE02B2B
        )
        await interaction.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Goblin(bot))

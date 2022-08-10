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

from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.config import load_config_cli, load_config
from chia.util.ints import uint16
from chia.util.bech32m import decode_puzzle_hash

# Here we name the cog and create a new class for the cog.
class Goblin(commands.Cog, name="goblin-slash"):
    def __init__(self, bot):
        self.bot = bot
        self.addresses = {}
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
        try:
            client = await FullNodeRpcClient.create('10.0.0.2', uint16(self.full_node_rpc_port), DEFAULT_ROOT_PATH, self.config)
            records = await client.get_coin_records_by_puzzle_hash(decode_puzzle_hash("xch14qdfrt7lkw9hkeg60qqunp6utzzw4flwgj7l7h7mmcmwzjkwxdes3njv47"))

            print(records)
        finally:
            client.close()

        embed = disnake.Embed(
            title="Address set",
            description="Set address: ",
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
    async def myaddress(self, interaction: ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Your Goblin Army Address",
            description="Your address is: " + self.addresses[interaction.author.id],
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
    async def setgoblinaddress(self, interaction: ApplicationCommandInteraction, address: str=""):

        self.addresses[interaction.author.id] = address
        embed = disnake.Embed(
            title="Address set",
            description="Set address " + address + " for: " + str(interaction.author),
            color=0xE02B2B
        )
        await interaction.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Goblin(bot))

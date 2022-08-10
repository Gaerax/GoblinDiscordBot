""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1.1
"""

import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Goblin(commands.Cog, name="goblin-normal"):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(
    #     name="goblinstats",
    #     description="Gets the stats of a goblin by number",
    # )
    # @checks.not_blacklisted()
    # @checks.is_owner()
    # async def goblinstats(self, context: Context) -> None:
    #     """
    #     This is a testing command that does nothing.
    #     :param context: The context in which the command has been executed.
    #     """
    #     embed = disnake.Embed(
    #         title="Address set",
    #         description="Set address ",
    #         color=0xE02B2B
    #     )
    #     await context.send(embed=embed)

    # @commands.command(
    #     name="setgoblinaddress",
    #     description="Set the xch address of your goblin army",
    # )
    # @checks.not_blacklisted()
    # @checks.is_owner()
    # async def setgoblinaddress(self, context: Context, member: disnake.Member, address: str) -> None:
    #     """
    #     This is a testing command that does nothing.
    #     :param context: The context in which the command has been executed.
    #     """
    #     embed = disnake.Embed(
    #         title="Address set",
    #         description="Set address for: ",
    #         color=0xE02B2B
    #     )
    #     await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Goblin(bot))

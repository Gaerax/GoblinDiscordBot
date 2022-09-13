import disnake
import time
import random
import json
import asyncio
from helpers import goblinhelper
from helpers import chiahelper


class DualPostView(disnake.ui.View):
    def __init__(self, interaction, user: disnake.user, useraddress, usergoblins, opponent: disnake.user, opponentaddress, opponentgoblins, deathbattle):
        super().__init__(timeout=90)
        self.interaction = interaction
        self.user = user
        self.useraddress = useraddress
        self.opponent = opponent
        self.opponentaddress = opponentaddress
        if len(usergoblins) > 24:
            self.usergoblins = random.sample(usergoblins,24)
        else:
            self.usergoblins = usergoblins
        if len(opponentgoblins) > 24:
            self.opponentgoblins = random.sample(opponentgoblins,24)
        else:
            self.opponentgoblins = opponentgoblins
        self.userbet = None
        self.opponentbet = None
        self.deathbattle = deathbattle
        for child in self.children:
            if child.custom_id == "usergoblins":
                for g in self.usergoblins:
                    child.append_option(g)
            if child.custom_id == "opponentgoblins":
                for g in self.opponentgoblins:
                    child.append_option(g)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return (
            (interaction.author == self.interaction.author or interaction.author == self.opponent)
            and interaction.channel == self.interaction.channel
        )

    async def on_timeout(self) -> None:
        await self.interaction.delete_original_message()

    @disnake.ui.select(placeholder=f"You are betting", min_values=1, max_values=1, options=["Nothing"], custom_id="usergoblins")
    async def user_goblin_select(self, select: disnake.ui.Select, interaction: disnake.MessageInteraction):
        if interaction.author == self.user:
            select.disabled = True
            self.userbet = select.values
            await interaction.response.defer()

    @disnake.ui.select(placeholder=f"For opponents", min_values=1, max_values=1, options=["Nothing"], custom_id="opponentgoblins")
    async def opponent_goblin_select(self, select: disnake.ui.Select, interaction: disnake.MessageInteraction):
        if interaction.author == self.user:
            select.disabled = True
            self.opponentbet = select.values
            await interaction.response.defer()

    @disnake.ui.button(label="Post Dual", style=disnake.ButtonStyle.green)
    async def post_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.user:
            await interaction.response.defer()
            view = DualAcceptView(interaction, self.user, self.useraddress, self.usergoblins, self.opponent, self.opponentaddress, self.opponentgoblins, self.deathbattle, self.userbet, self.opponentbet)
            embed = disnake.Embed(
                title=f"{self.user.display_name} Proposed a 1v1 Dual",
                description=f"{self.user.mention} vs {self.opponent.mention}",
                color=0x666666
            )
            embed.add_field(name=f"{self.user.display_name}'s goblin", value=f"{self.userbet[0]}", inline=True)
            embed.add_field(name=f"{self.opponent.display_name}'s goblin", value=f"{self.opponentbet[0]}", inline=True)
            await self.interaction.edit_original_message(view=view, embed=embed, allowed_mentions=disnake.AllowedMentions(users=True))


    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.danger)
    async def cancel_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.user:
            await self.interaction.delete_original_message()


class DualAcceptView(disnake.ui.View):
    def __init__(self, interaction, user: disnake.user, useraddress, usergoblins, opponent: disnake.user, opponentaddress, opponentgoblins, deathbattle, userbet, opponentbet):
        super().__init__(timeout=60*60*8)
        self.interaction = interaction
        self.user = user
        self.useraddress = useraddress
        self.usergoblins = usergoblins
        self.opponent = opponent
        self.opponentaddress = opponentaddress
        self.opponentgoblins = opponentgoblins
        self.userbet = userbet
        self.opponentbet = opponentbet
        self.deathbattle = deathbattle

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return (
            (interaction.author == self.interaction.author or interaction.author == self.opponent)
            and interaction.channel == self.interaction.channel
        )

    async def on_timeout(self) -> None:
        await self.interaction.delete_original_message()

    @disnake.ui.button(label="Accept", style=disnake.ButtonStyle.green)
    async def accept_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.opponent:
            await interaction.response.defer()
            view = DualView(interaction, self.user, self.useraddress, self.usergoblins, self.opponent, self.opponentaddress, self.opponentgoblins, self.deathbattle, self.userbet, self.opponentbet)
            await view.start_battle()


    @disnake.ui.button(label="Decline", style=disnake.ButtonStyle.danger)
    async def decline_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.opponent:
            await interaction.response.defer()
            embed = disnake.Embed(
                title=f"{self.opponent.display_name} declined {self.user.display_name}'s Dual",
                description=f"This duel is no longer valid.",
                color=0x666666
            )
            await self.interaction.delete_original_message()
            await self.interaction.send(embed=embed, allowed_mentions=disnake.AllowedMentions(users=True))



class DualView(disnake.ui.View):
    def __init__(self, interaction, user: disnake.user, useraddress, usergoblins, opponent: disnake.user, opponentaddress, opponentgoblins, deathbattle, userbet, opponentbet):
        super().__init__()
        self.interaction = interaction
        self.user = user
        self.useraddress = useraddress
        self.usergoblins = usergoblins
        self.opponent = opponent
        self.opponentaddress = opponentaddress
        self.opponentgoblins = opponentgoblins
        self.userbet = userbet
        self.opponentbet = opponentbet
        self.deathbattle = deathbattle

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return (
            interaction.author == self.interaction.author
            and interaction.channel == self.interaction.channel
        )

    async def on_timeout(self) -> None:
        await self.interaction.delete_original_message()

    async def start_battle(self):
        winnermessages = [
            "To the winner go the spoils!",
            "You army is strong!",
            "Jingle jingle, your bag of gold gets heavier!"
        ]
        embed = disnake.Embed(
            title="1v1 Dual",
            description=f"{self.user.mention} vs {self.opponent.mention}",
            color=0x222222
        )
        usergoblin = goblinhelper.getGoblinStats(int(self.userbet[0].split("#")[1]))
        opponentgoblin = goblinhelper.getGoblinStats(int(self.opponentbet[0].split("#")[1]))
        userhp = usergoblin["Battle Stats"]["Health"]
        opponenthp = opponentgoblin["Battle Stats"]["Health"]

        userfighter = embed.add_field(name=self.user.display_name, value=f"{self.userbet[0]} | {userhp}hp", inline=False)
        opponentfighter = embed.add_field(name=self.opponent.display_name, value=f"{self.opponentbet[0]} | {opponenthp}hp", inline=False)
        await self.interaction.edit_original_message(view=None, embed=embed, allowed_mentions=disnake.AllowedMentions(users=True))

        userattackcooldown = 50 - usergoblin["Battle Stats"]["Attack Speed"]
        opponentattackcooldown = 50 - opponentgoblin["Battle Stats"]["Attack Speed"]
        random.seed(time.time())
        while userhp > 0 and opponenthp > 0:
            await asyncio.sleep(0.01)
            userattackcooldown -= 1
            opponentattackcooldown -= 1
            changed = False
            if userattackcooldown < 0:
                userattackcooldown = 50 - usergoblin["Battle Stats"]["Attack Speed"]
                acc = usergoblin["Battle Stats"]["Accuracy"] - ((opponentgoblin["Battle Stats"]["Evasion"]/50)*usergoblin["Battle Stats"]["Accuracy"])
                r = random.randint(1, 40)
                if r < acc:
                    changed = True
                    dmg = usergoblin["Battle Stats"]["Attack Damage"] - ((opponentgoblin["Battle Stats"]["Defence"]/20)*usergoblin["Battle Stats"]["Attack Damage"])
                    dmg -= random.random() * usergoblin["Battle Stats"]["Attack Damage"]/2
                    opponenthp -= dmg

            if opponentattackcooldown < 0:
                opponentattackcooldown = 50 - opponentgoblin["Battle Stats"]["Attack Speed"]
                acc = opponentgoblin["Battle Stats"]["Accuracy"] - ((usergoblin["Battle Stats"]["Evasion"]/50)*opponentgoblin["Battle Stats"]["Accuracy"])
                r = random.randint(1, 40)
                if r < acc:
                    changed = True
                    dmg = opponentgoblin["Battle Stats"]["Attack Damage"] - ((usergoblin["Battle Stats"]["Defence"]/20)*opponentgoblin["Battle Stats"]["Attack Damage"])
                    dmg -= random.random() * opponentgoblin["Battle Stats"]["Attack Damage"]/2
                    userhp -= dmg

            if changed:
                embed.clear_fields()
                userfighter = embed.add_field(name=self.user.display_name, value=f"{self.userbet[0]} | {userhp:.0f}hp", inline=False)
                opponentfighter = embed.add_field(name=self.opponent.display_name, value=f"{self.opponentbet[0]} | {opponenthp:.0f}hp", inline=False)
                await self.interaction.edit_original_message(embed=embed)
            changed = False

        if userhp > opponenthp:
            if self.deathbattle:
                usergoblin["Experience"] += 300
            else:
                usergoblin["Experience"] += 100
            opponentgoblin["Experience"] = 0
            opponentgoblin["Level"] = 1
            log = {
                "deathbattle": self.deathbattle,
                "winner": usergoblin,
                "loser": opponentgoblin
            }
            if self.deathbattle:
                winnergold = 100
                embed = disnake.Embed(
                    title=f"{self.user.display_name} WINS!!!",
                    description=f"{self.opponent.mention} must transfer {self.opponentbet[0]} to {self.user.mention}!",
                    color=0x333333
                )
                embed.add_field(name="Winner address", value=self.useraddress, inline=False)
            else:
                winnergold = 25
                embed = disnake.Embed(
                    title=f"{self.user.display_name} WINS!!!",
                    description=f"{self.opponentbet[0]} has been defeated!",
                    color=0x333333
                )
            embed.set_image(file=disnake.File(f"GoblinData/img/{int(self.userbet[0].split('#')[1])}.jpg"))
            await self.interaction.send(embed=embed, allowed_mentions=disnake.AllowedMentions(users=True))

            embed = await chiahelper.sendgold(self.user, winnergold, self.useraddress, f"{winnergold} gold")
            await self.interaction.send(embed=embed)
        else:
            if self.deathbattle:
                opponentgoblin["Experience"] += 300
            else:
                opponentgoblin["Experience"] += 100
            usergoblin["Experience"] = 0
            log = {
                "deathbattle": self.deathbattle,
                "winner": opponentgoblin,
                "loser": usergoblin
            }
            if self.deathbattle:
                winnergold = 100
                embed = disnake.Embed(
                    title=f"{self.user.display_name} WINS!!!",
                    description=f"{self.opponent.mention} must transfer {self.opponentbet[0]} to {self.user.mention}!",
                    color=0x333333
                )
                embed.add_field(name="Winner address", value=self.useraddress, inline=False)
            else:
                winnergold = 25
                embed = disnake.Embed(
                    title=f"{self.user.display_name} WINS!!!",
                    description=f"{self.userbet[0]} has been defeated!",
                    color=0x333333
                )
            embed.set_image(file=disnake.File(f"GoblinData/img/{int(self.opponentbet[0].split('#')[1])}.jpg"))
            await self.interaction.send(embed=embed, allowed_mentions=disnake.AllowedMentions(users=True))

            embed = await chiahelper.sendgold(self.opponent, winnergold, self.opponentaddress, f"{self.opponent.display_name} earned {winnergold} gold!\n{random.choice(winnermessages)}")
            await self.interaction.send(embed=embed)

        logfile = open(f"DuelLogs/{self.userbet[0].split('#')[1]}v{self.opponentbet[0].split('#')[1]}-{int(time.time())}.json", "w")
        json.dump(log, logfile, indent=4)
        logfile.close()

        goblinhelper.updateStats(int(self.userbet[0].split('#')[1]), usergoblin)
        goblinhelper.updateStats(int(self.opponentbet[0].split('#')[1]), opponentgoblin)

"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from asyncio import sleep
from discord import app_commands, Interaction
from discord.app_commands import Choice
from discord.ext import commands
from cogs.utils.functions import add_xp
from cogs.utils.database.fetchdata import create_wallet
from cogs.utils.cooldown import set_cooldown
from cogs.utils.constants import Game, Emojis
from cogs.utils.functions import balance_check
from random import randint


MAX_BET_VALUE = Game.max_bet_value
morelicash = Emojis.morelicash
cross = Emojis.cross
coinfront = Emojis.coinfront
coinback = Emojis.coinback

class Gambles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def interaction_check(self, interaction: Interaction) -> bool:

        user = interaction.user
        data = interaction.namespace
        """
        * Interaction.data gives us only the first option
        * Interaction.namespace gives all options for the command
        """

        for i in data:
            if i[0] == "amount": # i[0] is Option name
                value = i[1] # i[1] is Option value 
                user_data, _ = await create_wallet(self.bot, user.id)
                check = await balance_check(interaction, user_data["cash"], value)

                if check:
                    await add_xp(self.bot, user.id, "gambler_xp")
                    return True
                return False
        return False

    @app_commands.command(
            name="coinflip", 
            description="Play coinflip",
            extras={
                'category': 'gamble',
                'help': "Yazı-Tura atarak paranızı katlayın."
            })
    @app_commands.describe(amount="Enter the bet amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    async def coinflip(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE]):
        user = interaction.user
        user_data, collection = await create_wallet(self.bot, user.id)

        num = randint(0,1)
        message = ""
        if num == 1:
            user_data["cash"] += amount * 2
            message = f"{coinfront} Tebrikler! Coinflip oyunundan tam **{amount*2:,}LC** kazandınız."
        else:
            user_data["cash"] -= amount
            message = f"{coinback} Maalesef kaybettiniz;c **~~{amount:,}LC~~**"

        await collection.replace_one({"_id": user.id}, user_data)
        await interaction.response.send_message(content = message)

    @app_commands.command(
            name="guess-number", 
            description="[1-5] Guess the number and make LiCash",
            extras={
                'category': 'gamble',
                'help': "[1-5] arası sayıyı tahmin edin ve paranızı katlayın." 
            })
    @app_commands.describe(guessnum="Enter your guess [1-5]", amount="Enter the bet amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    async def guessnumber(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE], guessnum: app_commands.Range[int, 1,5]):
        user = interaction.user
        user_data, collection = await create_wallet(self.bot, user.id)

        num = randint(1,5)
        message = ""
        if guessnum == num:
            message = f"{morelicash} Tebrikler! **{num}** rakamını doğru tahmin ettiniz ve tam **{amount:,}LC** kazandınız."
            user_data["cash"] += amount * 2
        else:
            message = f"{cross} Maalesef kaybettiniz;c **{num}** rakamını doğru tahmin edemediniz. **~~{amount:,}LC~~**"
            user_data["cash"] -= amount

        await collection.replace_one({"_id": user.id}, user_data)
        await interaction.response.send_message(content = message)

    @app_commands.command(
            name="roll", 
            description="Roll the dice and make LiCash",
            extras={
                'category': 'gamble',
                'help': "İki zarın toplam sonucunun çift mi, tek mi olacağını tahmin edin."
            })
    @app_commands.describe(choose="Choose", amount="Enter the bet amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    @app_commands.choices(choose = [
        Choice(name="Çift", value="0"),
        Choice(name="Tek", value="1")
    ])
    async def roll(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE], choose: str):

        user = interaction.user
        user_data, collection = await create_wallet(self.bot, user.id)

        dice = randint(2,12)
        message = ""

        if (dice % 2 == 0 and int(choose) == 0) or (dice % 2 != 0 and int(choose) == 1):
            user_data["cash"] += amount * 2
            message = f"{morelicash} Tebrikler! Iki zar sonucu **{dice}** geldi ve tam **{amount*2:,}LC** kazandınız."
        else:
            user_data["cash"] -= amount
            message = f"{cross} Maalesef kaybettiniz;c Iki zar sonucu **{dice}** geldi. **~~{amount:,}LC~~**"

        await collection.replace_one({"_id": user.id}, user_data)
        await interaction.response.send_message(content = ":game_die: Zarlar atılıyor...")
        await sleep(3)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Gambles(bot))

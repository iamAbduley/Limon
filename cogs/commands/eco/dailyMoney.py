"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction
from discord.ext import commands
from cogs.utils.constants import Emojis
from cogs.utils.database.fetchdata import create_wallet


wallet = Emojis.limonbank
morelicash = Emojis.morelicash
clock = Emojis.clock

class DailyMoney(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Günlük LiCash'inizi alın.")
    async def daily_money(self, interaction: Interaction):

        user_data, collection = await create_wallet(self.bot, interaction.user.id)
        
        accumulated_money = user_data["accumulated_money"]
        user_money = user_data["cash"]

        user_money += accumulated_money
        accumulated_money = 0

        await collection.replace_one({"_id": interaction.user.id}, user_data)
        await interaction.response.send_message(content = f"{morelicash} Günlük kazancınız **{accumulated_money:,}LC**")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(DailyMoney(bot))
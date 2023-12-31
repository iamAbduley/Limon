"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from .error import ErrorHandler
from discord.ext.commands import Bot

async def setup(bot: Bot):
    await bot.add_cog(ErrorHandler(bot))
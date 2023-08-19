"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from asyncio import sleep
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.utils.database.fetchdata import create_inventory_data
from cogs.utils.functions import add_point
from cogs.utils.constants import Emojis
from yaml import Loader, load
from random import choice, randint

basic_items_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
basic_item = load(basic_items_yaml, Loader=Loader)

mine_yaml = open("cogs/assets/yaml_files/job/yamls/mines.yml", "rb")
mines = load(mine_yaml, Loader=Loader)

class Mining(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def mine_goose(self):
        mine = choice(list(mines.keys()))
        name = mines[mine]["name"]
        weight = randint(10, 20)
        return name, weight, mine

    @app_commands.command(name="mining", description="Go mining!")
    async def mining(self, interaction: Interaction):

        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        if "mining" not in inventory["items"]:
            return await interaction.response.send_message(
                content=f"{Emojis.cross} Maden kazabilmek için bir madencilik ekipmanına sahip olmalısınız!",
                ephemeral=True)
        
        equipment = inventory["items"]["mining"]

        if equipment["durability"] < 4:
            return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanınız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)
        equipment["durability"] -= 4

        if basic_item["mining"][equipment]["type"] != "vehicle":
            average_mine = basic_item["mining"][equipment]["average_mine"]
            mine_count = randint(average_mine - 1, average_mine + 1)

            equipment["fuel"] -= (basic_item["mining"][equipment]["liter_per_mine"] * mine_count)

            excavated_mine = []
            for _ in range(mine_count):
                name, weight, mine = self.mine_goose()
                excavated_mine.append([name, weight])
                inventory["jobs_results"]["mines"].append(f"{mine}_{weight}")
                excavated_mine_ = [f":diamond: {mine[0]} - {mine[1]}m\n" for mine_list in excavated_mine for mine in excavated_mine]
                message = f":pickaxe: Aracımız geri döndü. İşte çıkardığı madenler:\n{excavated_mine_}"

        else:
            name, weight, mine = self.mine_goose()

            message = ":diamond: Harika! Madenden {weight}kg ağırlığında {name} çıkardınız."
            inventory["jobs_results"]["mines"].append(f"{mine}_{weight}")

        await add_point(self.bot, user.id, "miner_xp")
        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.send_message(content = ":pickaxe: Madene iniyoruz..")
        await sleep(6)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mining(bot))
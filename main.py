import discord
from dotenv import load_dotenv
import os

from discord.ext import commands
import pathlib


load_dotenv()

API_KEY = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs():
    cogs_path = pathlib.Path("src/app/cogs")

    for cog_file in cogs_path.glob("*.py"):
        if cog_file.name != "__init__.py":
            module_name = str(cog_file).replace(os.sep, ".")[:-3]
            try:
                await bot.load_extension(module_name)
                print(f"Successfullly loaded extension: {module_name}")
            except commands.ExtensionNotFound as e:
                print(f"Failed to load extension {module_name} with error: {e}")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await load_cogs()
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)!")


bot.run(API_KEY)

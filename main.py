import discord
from dotenv import load_dotenv
import os

from src.app.utils import get_secret

load_dotenv()

API_KEY = os.getenv("API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print (f"We have logged in as {client.user}")
    await tree.sync()
    print("commands synced!")



@client.event
async def on_message(message: discord.message.Message):
    if message.author == client.user:
        return
    
    if message.content.startswith('hello bot'):
        await message.channel.send("Hello!")

@tree.command(name="test", description="Test if bot is working")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Slash command is working")

print(get_secret("api_key"))
client.run(get_secret("api_key"))



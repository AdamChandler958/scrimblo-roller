import discord
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print (f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('hello bot'):
        await message.channel.send("Hello!")


client.run(API_KEY)



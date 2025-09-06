
import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.app_commands.command(name="test", description="Test if bot is working")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Slash command is working")

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        if message.author == self.bot.user:
            return
        
        if message.content.startswith('hello bot'):
            await message.channel.send("Hello from the Cog!")

async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCommands(bot))


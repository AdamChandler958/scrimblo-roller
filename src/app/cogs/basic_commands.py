
import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    """
    A cog for basic commands and event listeners.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.app_commands.command(name="test", description="Test if bot is working")
    async def test_command(self, interaction: discord.Interaction):
        """
        Tests if the bot is responsive by sending a message.

        Args:
            interaction (discord.Interaction): The interaction object.
        """

        await interaction.response.send_message("Slash command is working")

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        """
        Listens for messages and responds to a specific phrase.

        Args:
            message (discord.message.Message): The message object.
        """

        if message.author == self.bot.user:
            return
        
        if message.content.startswith('hello bot'):
            await message.channel.send("Hello from the Cog!")

async def setup(bot: commands.Bot):
    """
    Adds the BasicCommands cog to the bot.

    Args:
        bot (commands.Bot): The bot instance.
    """
    
    await bot.add_cog(BasicCommands(bot))


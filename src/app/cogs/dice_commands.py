import discord
from discord.ext import commands
from src.app.rolls import parse_dice_string

class DiceCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="roll", description="Roll some dice!")
    @discord.app_commands.describe(roll="The size and number of dice you wish to roll [Int currently]")
    async def roll_command(self, interaction: discord.Interaction, roll: str):
        await interaction.response.send_message(f"{roll}:\n ```{parse_dice_string(roll)}```")

async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCommands(bot))
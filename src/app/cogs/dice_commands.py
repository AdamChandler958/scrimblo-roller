import discord
from discord.ext import commands
from src.app.rolls import parse_dice_string

class DiceCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="roll", description="Roll some dice!")
    @discord.app_commands.describe(roll="The size and number of dice you wish to roll")
    async def roll_command(self, interaction: discord.Interaction, roll: str):

        dice_embedding = discord.Embed(
            title="Dice Roll Results",
            description=f"Results for `{roll}`",
            color=discord.Color.purple()
        )
        rolls_display, total = parse_dice_string(roll)

        dice_embedding.add_field(name="Rolls", value=rolls_display, inline=False)
        dice_embedding.add_field(name="Total", value=str(total), inline=False)

        await interaction.channel.send(embed=dice_embedding)


async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCommands(bot))
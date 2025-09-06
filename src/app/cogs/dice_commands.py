import discord
from discord.ext import commands
from src.app.rolls import DiceRoll

class DiceCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="roll", description="Roll some dice!")
    @discord.app_commands.describe(roll="The size and number of dice you wish to roll")
    async def roll_command(self, interaction: discord.Interaction, roll: str):

        dice_roll = DiceRoll(roll)
        dice_roll.perform_roll()
        response = dice_roll.get_result()

        if "error" in response:
            await interaction.response.send_message(response.get("error"), ephemeral=True)
            return


        dice_embedding = discord.Embed(
            title="Dice Roll Results",
            description=f"Results for `{response["expression"]}`",
            color=discord.Color.purple()
        )

        dice_embedding.add_field(name="Rolls", value=response["formatted_rolls"], inline=False)
        dice_embedding.add_field(name="Total", value=str(response["total"]), inline=False)

        await interaction.response.send_message(embed=dice_embedding)


async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCommands(bot))
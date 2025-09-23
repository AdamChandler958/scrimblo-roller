import discord
from discord.ext import commands
from src.app.rolls import DiceRoll

class DiceCommands(commands.Cog):
    """
    A cog for dice related commands and slash command listeners.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="roll", description="Roll some dice!")
    @discord.app_commands.describe(roll="The size and number of dice you wish to roll")
    async def roll_command(self, interaction: discord.Interaction, roll: str):
        """
        Listens for the /roll command within a text channel and returns the result of that roll as an embedded message.

        Args:
            interaction (discord.Interaction): The interaction object.
            roll (str): A plaintext request for the dice roll, optional modifiers, etc e.g ```1d20+8```
        """

        dice_roll = DiceRoll(roll)
        dice_roll.perform_roll()
        response = dice_roll.get_result()

        if "error" in response:
            await interaction.response.send_message(response.get("error"), ephemeral=True)
            return


        dice_embedding = discord.Embed(
            title=response["comment"],
            description=f"Results for `{response["expression"]}`",
            color=discord.Color.purple()
        )

        dice_embedding.add_field(name="Rolls", value=response["formatted_result_string"], inline=False)
        dice_embedding.add_field(name="Total", value=str(response["grand_total"]), inline=False)

        await interaction.response.send_message(embed=dice_embedding)


async def setup(bot: commands.Bot):
    """
    Adds the DiceCommands cog to the bot.

    Args:
        bot (commands.Bot): The bot instance.
    """
    
    await bot.add_cog(DiceCommands(bot))
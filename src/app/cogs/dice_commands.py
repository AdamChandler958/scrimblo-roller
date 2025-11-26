import discord
from discord.ext import commands
from src.app.rolls import DiceRoll
from src.app.vtm import VtMRolls


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
    @discord.app_commands.describe(
        is_milky="If you want the total to appear as the comment"
    )
    async def roll_command(
        self, interaction: discord.Interaction, roll: str, is_milky: bool = False
    ):
        """
        Parses a plain text dice command and generates an embedded output.

        Examples:
        - `2d20+5`: Roll two 20-sided dice and add 5.
        - `3d6kh2`: Roll three 6-sided dice and keep the 2 highest results.
        - `d10-3`: Roll one 10-sided die and subtract 3.
        - `10`: A simple modifier of 10.
        - `2d4-1+2d8 This is a comment`: Multiple dice rolls and a comment.
        """

        dice_roll = DiceRoll(roll)
        dice_roll.perform_roll()
        response = dice_roll.get_result()

        if "error" in response:
            await interaction.response.send_message(
                response.get("error"), ephemeral=True
            )
            return

        if is_milky:
            dice_embedding = discord.Embed(
                title=str(response["grand_total"]),
                description=f"Results for `{response['expression']}`",
                color=discord.Color.purple(),
            )

            dice_embedding.add_field(
                name="Rolls", value=response["formatted_result_string"], inline=False
            )
            if response["comment"] != "":
                dice_embedding.add_field(
                    name="Comment", value=response["comment"], inline=False
                )

        else:
            dice_embedding = discord.Embed(
                title=response["comment"]
                if response["comment"] != ""
                else "Dice Results for Roll.",
                description=f"Results for `{response['expression']}`",
                color=discord.Color.purple(),
            )

            dice_embedding.add_field(
                name="Rolls", value=response["formatted_result_string"], inline=False
            )
            dice_embedding.add_field(
                name="Total", value=str(response["grand_total"]), inline=False
            )

        await interaction.response.send_message(embed=dice_embedding)

    @discord.app_commands.command(name="vtm", description="Roll some dice Kindred!")
    @discord.app_commands.describe(dice_pool="Size of the dice pool")
    @discord.app_commands.describe(hunger="Number of Hunger Dice")
    async def vtm(
        self, interaction: discord.Interaction, dice_pool: int, hunger: int = None
    ):
        """"""

        dice_roll = VtMRolls(dice_pool, hunger)
        dice_roll.generate()

        try:
            response = dice_roll.format_result()
        except Exception as e:
            await interaction.response.send_message(
                f"Error in format {e}", ephemeral=True
            )

        dice_embedding = discord.Embed(
            title=response["overall_result"],
            description=f"Results for dice pool of {dice_pool} and hunger {hunger}"
            if hunger is not None
            else f"Results for dice pool of {dice_pool}",
            color=discord.Color.dark_red(),
        )

        dice_embedding.add_field(name="Rolls", value=response["squares"], inline=False)

        await interaction.response.send_message(embed=dice_embedding)


async def setup(bot: commands.Bot):
    """
    Adds the DiceCommands cog to the bot.

    Args:
        bot (commands.Bot): The bot instance.
    """

    await bot.add_cog(DiceCommands(bot))

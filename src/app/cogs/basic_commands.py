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
        await interaction.response.send_message("Slash command is working")

    @discord.app_commands.command(
        name="help", description="Shows information on available commands."
    )
    async def help_command(self, interaction: discord.Interaction):
        """
        Dynamically generates and sends a help message for all registered slash commands.
        """

        embed = discord.Embed(
            title="Bot Help",
            description="Here are all the available slash commands:",
            color=discord.Color.blue(),
        )

        for command in self.bot.tree.walk_commands():
            name = command.name
            description = command.description or "No description provided."

            docstring = command.callback.__doc__

            if docstring:
                usage_info = docstring.strip()
            else:
                usage_info = "No usage information available."

            embed.add_field(
                name=f"/{name}",
                value=f"**Description:** {description}\n**Usage:** {usage_info}",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """
    Adds the BasicCommands cog to the bot.

    Args:
        bot (commands.Bot): The bot instance.
    """

    await bot.add_cog(BasicCommands(bot))

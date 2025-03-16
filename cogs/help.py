
import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Shows all available commands')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are all the available commands:",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )

        for cog in self.bot.cogs.values():
            commands_list = []
            for command in cog.get_app_commands():
                commands_list.append(f"`/{command.name}` - {command.description}")
            
            if commands_list:
                embed.add_field(
                    name=cog.__class__.__name__,
                    value="\n".join(commands_list),
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
  

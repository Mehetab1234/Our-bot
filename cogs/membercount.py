import discord
from discord.ext import commands
from discord import app_commands

class MemberCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='membercount', description='Shows the current member count')
    async def member_count(self, interaction: discord.Interaction):
        try:
            total_members = interaction.guild.member_count
            online_members = len([m for m in interaction.guild.members if m.status != discord.Status.offline])

            embed = discord.Embed(title="Server Statistics", color=discord.Color.blue())
            embed.add_field(name="Total Members", value=str(total_members), inline=True)
            embed.add_field(name="Online Members", value=str(online_members), inline=True)
            embed.set_footer(text=f"Requested by {interaction.user.name}")

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error getting member count: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MemberCount(bot))
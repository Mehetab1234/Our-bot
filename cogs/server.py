import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_settings = {}

    @app_commands.command(name='slowmode', description='Set slowmode for the current channel')
    @app_commands.describe(seconds='Slowmode delay in seconds (0 to disable)')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.response.send_message("Slowmode has been disabled.")
            else:
                await interaction.response.send_message(f"Slowmode set to {seconds} seconds.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change slowmode.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error setting slowmode: {str(e)}", ephemeral=True)

    @app_commands.command(name='lock', description='Lock the current channel')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        try:
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
            await interaction.response.send_message("🔒 Channel has been locked.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to lock the channel.", ephemeral=True)

    @app_commands.command(name='unlock', description='Unlock the current channel')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        try:
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=None)
            await interaction.response.send_message("🔓 Channel has been unlocked.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unlock the channel.", ephemeral=True)

    @app_commands.command(name='nickname', description='Change a member\'s nickname')
    @app_commands.describe(member='The member to change nickname for', nickname='The new nickname')
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nickname(self, interaction: discord.Interaction, member: discord.Member, nickname: str = None):
        try:
            await member.edit(nick=nickname)
            if nickname:
                await interaction.response.send_message(f"Changed {member.name}'s nickname to {nickname}")
            else:
                await interaction.response.send_message(f"Reset {member.name}'s nickname")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change that member's nickname.", ephemeral=True)

    @app_commands.command(name='setdelay', description='Set message deletion delay for auto-mod')
    @app_commands.describe(seconds='Delay in seconds before deleting flagged messages')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def setdelay(self, interaction: discord.Interaction, seconds: int):
        if seconds < 0:
            await interaction.response.send_message("Please specify a positive number of seconds.", ephemeral=True)
            return
            
        self.channel_settings[interaction.channel.id] = seconds
        await interaction.response.send_message(f"Auto-mod message deletion delay set to {seconds} seconds.")

async def setup(bot):
    await bot.add_cog(Server(bot))

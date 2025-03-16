import discord
from discord.ext import commands
from discord import app_commands
import datetime
from typing import Optional

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='createvc', description='Create a new voice channel')
    @app_commands.describe(name='Name of the voice channel', limit='User limit (optional)')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def createvc(self, interaction: discord.Interaction, name: str, limit: Optional[int] = None):
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(connect=True)
            }
            channel = await interaction.guild.create_voice_channel(
                name=name,
                user_limit=limit,
                overwrites=overwrites
            )
            await interaction.response.send_message(f"Created voice channel: {channel.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to create voice channels.", ephemeral=True)

    @app_commands.command(name='vcmute', description='Mute all users in a voice channel')
    @app_commands.describe(channel='The voice channel to mute')
    @app_commands.checks.has_permissions(mute_members=True)
    async def vcmute(self, interaction: discord.Interaction, channel: Optional[discord.VoiceChannel] = None):
        channel = channel or interaction.user.voice.channel if interaction.user.voice else None
        if not channel:
            await interaction.response.send_message("Please specify a voice channel or join one.", ephemeral=True)
            return

        try:
            for member in channel.members:
                await member.edit(mute=True)
            await interaction.response.send_message(f"Muted all users in {channel.name}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to mute members.", ephemeral=True)

    @app_commands.command(name='vcunmute', description='Unmute all users in a voice channel')
    @app_commands.describe(channel='The voice channel to unmute')
    @app_commands.checks.has_permissions(mute_members=True)
    async def vcunmute(self, interaction: discord.Interaction, channel: Optional[discord.VoiceChannel] = None):
        channel = channel or interaction.user.voice.channel if interaction.user.voice else None
        if not channel:
            await interaction.response.send_message("Please specify a voice channel or join one.", ephemeral=True)
            return

        try:
            for member in channel.members:
                await member.edit(mute=False)
            await interaction.response.send_message(f"Unmuted all users in {channel.name}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unmute members.", ephemeral=True)

    @app_commands.command(name='vckick', description='Kick a user from voice channel')
    @app_commands.describe(member='The member to kick from voice channel')
    @app_commands.checks.has_permissions(move_members=True)
    async def vckick(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice:
            await interaction.response.send_message("This user is not in a voice channel.", ephemeral=True)
            return

        try:
            await member.edit(voice_channel=None)
            await interaction.response.send_message(f"Kicked {member.name} from voice channel.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to disconnect members.", ephemeral=True)

    @app_commands.command(name='vcinfo', description='Show information about voice channels')
    async def vcinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Voice Channel Information",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )

        voice_channels = interaction.guild.voice_channels
        total_users = sum(len(vc.members) for vc in voice_channels)

        for vc in voice_channels:
            members = len(vc.members)
            member_list = ", ".join(m.name for m in vc.members) if members > 0 else "Empty"
            embed.add_field(
                name=f"{vc.name} ({members} users)",
                value=f"Limit: {vc.user_limit if vc.user_limit else 'None'}\nMembers: {member_list}",
                inline=False
            )

        embed.set_footer(text=f"Total users in voice: {total_users}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Voice(bot))
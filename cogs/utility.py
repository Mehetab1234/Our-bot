import discord
from discord.ext import commands
from discord import app_commands
import datetime
from typing import Optional

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channels = {}

    @app_commands.command(name='send', description='Send a message to the current channel')
    @app_commands.describe(message='The message to send')
    async def send_message(self, interaction: discord.Interaction, message: str):
        try:
            embed = discord.Embed(
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text=f"Sent by {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error sending message: {str(e)}", ephemeral=True)

    @app_commands.command(name='announce', description='Make an announcement in the current channel')
    @app_commands.describe(message='The announcement message')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def announce(self, interaction: discord.Interaction, message: str):
        try:
            embed = discord.Embed(
                title="📢 Announcement",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text=f"Announced by {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error making announcement: {str(e)}", ephemeral=True)

    @app_commands.command(name='serverinfo', description='Shows server information')
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"📊 {guild.name} Server Information",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )

        # Server info
        embed.add_field(name="Server Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Server Owner", value=guild.owner.name, inline=True)

        # Member stats
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = total_members - humans

        embed.add_field(name="Total Members", value=total_members, inline=True)
        embed.add_field(name="Humans", value=humans, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)

        # Channel stats
        channels = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)

        embed.add_field(name="Total Channels", value=channels, inline=True)
        embed.add_field(name="Text Channels", value=text_channels, inline=True)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=True)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='userinfo', description='Shows information about a user')
    @app_commands.describe(member='The user to get information about')
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        roles = [role.name for role in member.roles[1:]]  # Exclude @everyone
        embed = discord.Embed(
            title=f"👤 User Information - {member.name}",
            color=member.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick if member.nick else "None", inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.name, inline=True)
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=True)

        if roles:
            embed.add_field(name=f"Roles [{len(roles)}]", value=", ".join(roles) if len(roles) < 10 else f"{len(roles)} roles", inline=False)

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='setwelcome', description='Set the welcome channel for new members')
    @app_commands.describe(channel='The channel to send welcome messages in')
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcome(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        self.welcome_channels[interaction.guild.id] = channel.id
        await interaction.response.send_message(f"Welcome messages will now be sent to {channel.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id in self.welcome_channels:
            channel = self.bot.get_channel(self.welcome_channels[member.guild.id])
            if channel:
                embed = discord.Embed(
                    title="👋 Welcome!",
                    description=f"Welcome {member.mention} to {member.guild.name}!\nWe hope you enjoy your stay!",
                    color=discord.Color.green()
                )
                if member.avatar:
                    embed.set_thumbnail(url=member.avatar.url)
                await channel.send(embed=embed)

    @app_commands.command(name='pin', description='Pin a message to the channel')
    @app_commands.describe(message_id='ID of the message to pin')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def pin_message(self, interaction: discord.Interaction, message_id: str):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            await message.pin()
            await interaction.response.send_message("Message pinned successfully!", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Message not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to pin messages.", ephemeral=True)

    @app_commands.command(name='unpin', description='Unpin a message from the channel')
    @app_commands.describe(message_id='ID of the message to unpin')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unpin_message(self, interaction: discord.Interaction, message_id: str):
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            await message.unpin()
            await interaction.response.send_message("Message unpinned successfully!", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Message not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to unpin messages.", ephemeral=True)

    @app_commands.command(name='cleanup', description='Delete bot\'s own messages')
    @app_commands.describe(limit='Number of messages to check')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def cleanup(self, interaction: discord.Interaction, limit: int = 100):
        try:
            deleted = 0
            async for message in interaction.channel.history(limit=limit):
                if message.author == self.bot.user:
                    await message.delete()
                    deleted += 1
            await interaction.response.send_message(f"Deleted {deleted} bot messages.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages.", ephemeral=True)

    @app_commands.command(name='moveall', description='Move all members from one voice channel to another')
    @app_commands.describe(
        source='Source voice channel',
        destination='Destination voice channel'
    )
    @app_commands.checks.has_permissions(move_members=True)
    async def moveall(
        self,
        interaction: discord.Interaction,
        source: discord.VoiceChannel,
        destination: discord.VoiceChannel
    ):
        try:
            moved = 0
            for member in source.members:
                await member.move_to(destination)
                moved += 1
            await interaction.response.send_message(
                f"Moved {moved} members from {source.name} to {destination.name}",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to move members.", ephemeral=True)

    @app_commands.command(name='massrole', description='Add a role to multiple members')
    @app_commands.describe(
        role='The role to add',
        has_role='Only add to members who have this role (optional)'
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def massrole(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        has_role: Optional[discord.Role] = None
    ):
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I can't assign roles higher than my highest role.",
                ephemeral=True
            )
            return

        await interaction.response.defer()
        added = 0

        for member in interaction.guild.members:
            if has_role and has_role not in member.roles:
                continue
            try:
                if role not in member.roles:
                    await member.add_roles(role)
                    added += 1
            except discord.Forbidden:
                continue

        await interaction.followup.send(
            f"Added {role.name} to {added} members.",
            ephemeral=True
        )

    @app_commands.command(name='purgerole', description='Remove a role from all members')
    @app_commands.describe(role='The role to remove')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def purgerole(self, interaction: discord.Interaction, role: discord.Role):
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I can't remove roles higher than my highest role.",
                ephemeral=True
            )
            return

        await interaction.response.defer()
        removed = 0

        for member in interaction.guild.members:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    removed += 1
                except discord.Forbidden:
                    continue

        await interaction.followup.send(
            f"Removed {role.name} from {removed} members.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Utility(bot))
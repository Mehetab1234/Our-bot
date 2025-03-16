import discord
from discord.ext import commands
from discord import app_commands
import datetime
import platform

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @app_commands.command(name='botinfo', description='Shows information about the bot')
    async def botinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Information",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        
        # Calculate uptime
        uptime = datetime.datetime.utcnow() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        total_users = sum(guild.member_count for guild in self.bot.guilds)
        
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Total Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Total Users", value=str(total_users), inline=True)
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Uptime", value=f"{days}d {hours}h {minutes}m {seconds}s", inline=True)
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='channelinfo', description='Shows information about a channel')
    @app_commands.describe(channel='The channel to get information about')
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        
        embed = discord.Embed(
            title=f"Channel Information - #{channel.name}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
        embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="NSFW", value="Yes" if channel.is_nsfw() else "No", inline=True)
        embed.add_field(name="News Channel", value="Yes" if channel.is_news() else "No", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='roleinfo', description='Shows information about a role')
    @app_commands.describe(role='The role to get information about')
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(
            title=f"Role Information - {role.name}",
            color=role.color,
            timestamp=datetime.datetime.utcnow()
        )
        
        permissions = []
        if role.permissions.administrator:
            permissions.append("Administrator")
        if role.permissions.ban_members:
            permissions.append("Ban Members")
        if role.permissions.kick_members:
            permissions.append("Kick Members")
        if role.permissions.manage_messages:
            permissions.append("Manage Messages")
        if role.permissions.manage_roles:
            permissions.append("Manage Roles")
        
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        
        if permissions:
            embed.add_field(name="Key Permissions", value="\n".join(permissions), inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='emojiinfo', description='Shows information about server emojis')
    async def emojiinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"Emoji Information - {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        
        # Regular emojis
        static_emojis = [str(emoji) for emoji in guild.emojis if not emoji.animated]
        animated_emojis = [str(emoji) for emoji in guild.emojis if emoji.animated]
        
        embed.add_field(name="Static Emojis", value=len(static_emojis), inline=True)
        embed.add_field(name="Animated Emojis", value=len(animated_emojis), inline=True)
        embed.add_field(name="Total Emojis", value=len(guild.emojis), inline=True)
        
        if static_emojis:
            embed.add_field(name="Static Emoji List", value=" ".join(static_emojis[:20]) + 
                          ("..." if len(static_emojis) > 20 else ""), inline=False)
        if animated_emojis:
            embed.add_field(name="Animated Emoji List", value=" ".join(animated_emojis[:20]) + 
                          ("..." if len(animated_emojis) > 20 else ""), inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))

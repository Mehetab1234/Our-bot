import discord
from discord.ext import commands
from discord import app_commands
import datetime
from typing import Optional

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='createrole', description='Create a new role')
    @app_commands.describe(
        name='Role name',
        color='Role color (hex code)',
        hoist='Show role separately in member list',
        mentionable='Allow anyone to @mention this role'
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def createrole(
        self,
        interaction: discord.Interaction,
        name: str,
        color: Optional[str] = None,
        hoist: bool = False,
        mentionable: bool = False
    ):
        try:
            role_color = discord.Color.from_str(color) if color else discord.Color.default()
            role = await interaction.guild.create_role(
                name=name,
                color=role_color,
                hoist=hoist,
                mentionable=mentionable
            )
            await interaction.response.send_message(f"Created role: {role.mention}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid color format. Use hex color (e.g., #FF0000)", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to create roles.", ephemeral=True)

    @app_commands.command(name='giverole', description='Give a role to a member')
    @app_commands.describe(
        member='The member to give the role to',
        role='The role to give',
        reason='Reason for giving the role'
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def giverole(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
        reason: Optional[str] = None
    ):
        try:
            if role >= interaction.guild.me.top_role:
                await interaction.response.send_message("I can't assign roles higher than my highest role.", ephemeral=True)
                return
            await member.add_roles(role, reason=reason)
            await interaction.response.send_message(
                f"Given {role.name} to {member.name}" + (f" (Reason: {reason})" if reason else ""),
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)

    @app_commands.command(name='takerole', description='Remove a role from a member')
    @app_commands.describe(
        member='The member to remove the role from',
        role='The role to remove',
        reason='Reason for removing the role'
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def takerole(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
        reason: Optional[str] = None
    ):
        try:
            if role >= interaction.guild.me.top_role:
                await interaction.response.send_message("I can't remove roles higher than my highest role.", ephemeral=True)
                return
            await member.remove_roles(role, reason=reason)
            await interaction.response.send_message(
                f"Removed {role.name} from {member.name}" + (f" (Reason: {reason})" if reason else ""),
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)

    @app_commands.command(name='rolemembers', description='List all members with a specific role')
    @app_commands.describe(role='The role to list members for')
    async def rolemembers(self, interaction: discord.Interaction, role: discord.Role):
        members = role.members
        if not members:
            await interaction.response.send_message(f"No members have the {role.name} role.", ephemeral=True)
            return

        # Create pages of 20 members each
        members_per_page = 20
        pages = [members[i:i+members_per_page] for i in range(0, len(members), members_per_page)]

        for i, page in enumerate(pages, 1):
            embed = discord.Embed(
                title=f"Members with {role.name} role (Page {i}/{len(pages)})",
                color=role.color,
                timestamp=datetime.datetime.utcnow()
            )

            member_list = "\n".join(f"• {member.name}" for member in page)
            embed.description = member_list

            if i == 1:
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.followup.send(embed=embed)

    @app_commands.command(name='rolecolor', description='Change a role\'s color')
    @app_commands.describe(role='The role to change', color='New color (hex code)')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def rolecolor(self, interaction: discord.Interaction, role: discord.Role, color: str):
        try:
            if role >= interaction.guild.me.top_role:
                await interaction.response.send_message("I can't modify roles higher than my highest role.", ephemeral=True)
                return

            new_color = discord.Color.from_str(color)
            await role.edit(color=new_color)
            await interaction.response.send_message(f"Changed {role.name}'s color to {color}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid color format. Use hex color (e.g., #FF0000)", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to modify roles.", ephemeral=True)

    @app_commands.command(name='makeroles', description='Create multiple roles at once')
    @app_commands.describe(
        names='Role names (comma-separated)',
        color='Base color (hex code, optional)',
        hoist='Show roles separately in member list'
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def makeroles(
        self,
        interaction: discord.Interaction,
        names: str,
        color: Optional[str] = None,
        hoist: bool = False
    ):
        try:
            role_names = [name.strip() for name in names.split(',')]
            if not role_names:
                await interaction.response.send_message("Please provide at least one role name.", ephemeral=True)
                return

            base_color = discord.Color.from_str(color) if color else discord.Color.default()
            created_roles = []

            await interaction.response.defer()

            for name in role_names:
                try:
                    role = await interaction.guild.create_role(
                        name=name,
                        color=base_color,
                        hoist=hoist
                    )
                    created_roles.append(role.name)
                except discord.Forbidden:
                    continue

            if created_roles:
                await interaction.followup.send(
                    f"Created roles: {', '.join(created_roles)}",
                    ephemeral=True
                )
            else:
                await interaction.followup.send("Failed to create any roles.", ephemeral=True)

        except ValueError:
            await interaction.followup.send("Invalid color format. Use hex color (e.g., #FF0000)", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to create roles.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roles(bot))
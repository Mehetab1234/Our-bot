import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Modal, TextInput
import asyncio

class TicketModal(Modal):
    def __init__(self):
        super().__init__(title="Create Ticket")
        self.add_item(TextInput(label="Subject", placeholder="Enter ticket subject", max_length=100))
        self.add_item(TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="Describe your issue"))

    async def on_submit(self, interaction: discord.Interaction):
        subject = self.children[0].value
        description = self.children[1].value

        # Create ticket channel
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")

        if not category:
            category = await guild.create_category("Tickets")

        channel_name = f"ticket-{interaction.user.name.lower()}"
        channel = await category.create_text_channel(channel_name)

        # Set permissions
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        # Send initial message
        embed = discord.Embed(title=f"Ticket: {subject}", description=description, color=discord.Color.green())
        embed.set_footer(text=f"Created by {interaction.user.name}")
        await channel.send(embed=embed)

        await interaction.response.send_message(f"Ticket created in {channel.mention}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        modal = TicketModal()
        await interaction.response.send_modal(modal)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ticketpanel', description='Creates a ticket panel')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Support Tickets",
            description="Click the button below to create a support ticket",
            color=discord.Color.blue()
        )

        view = TicketView()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name='closeticket', description='Closes the current ticket')
    async def close_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith('ticket-'):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)  # Use asyncio.sleep instead of delay parameter
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Modal, TextInput
import asyncio

# Ticket Modal for user input
class TicketModal(Modal):
    def __init__(self):
        super().__init__(title="Create Ticket")
        self.add_item(TextInput(label="Subject", placeholder="Enter ticket subject", max_length=100))
        self.add_item(TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="Describe your issue"))

    async def on_submit(self, interaction: discord.Interaction):
        subject = self.children[0].value
        description = self.children[1].value

        # Get guild and category
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")

        if not category:
            category = await guild.create_category("Tickets")

        # Create ticket channel
        channel_name = f"ticket-{interaction.user.name.lower()}"
        channel = await category.create_text_channel(channel_name)

        # Set permissions (Only user and staff can see)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        # Set channel topic (description)
        await channel.edit(topic=f"Ticket created by {interaction.user.name} | Subject: {subject}")

        # Embed with an image
        embed = discord.Embed(
            title=f"Ticket: {subject}",
            description=description,
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Created by {interaction.user.name}")
        embed.set_thumbnail(url="https://i.imgur.com/AfFp7pu.png")  # Change this to your desired image

        await channel.send(embed=embed)
        await interaction.response.send_message(f"Ticket created in {channel.mention}", ephemeral=True)

# Ticket View for creating tickets
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        modal = TicketModal()
        await interaction.response.send_modal(modal)

# Ticket Commands
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ticketpanel', description='Creates a ticket panel')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Click the button below to create a support ticket.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="https://i.imgur.com/AfFp7pu.png")  # Change this image if needed

        view = TicketView()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name='closeticket', description='Closes the current ticket')
    async def close_ticket(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith('ticket-'):
            await interaction.response.send_message("This command can only be used in ticket channels!", ephemeral=True)
            return

        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))

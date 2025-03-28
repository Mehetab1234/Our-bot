import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='clear', description='Clears specified number of messages')
    @app_commands.describe(amount='Number of messages to delete')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message("Please specify a positive number of messages to delete.", ephemeral=True)
            return

        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error clearing messages: {str(e)}", ephemeral=True)

    @app_commands.command(name='createpost', description='Create a post (Admin only)')
    @app_commands.describe(title='Post title', content='Post content')
    @app_commands.checks.has_permissions(administrator=True)
    async def create_post(self, interaction: discord.Interaction, title: str, content: str):
        try:
            embed = discord.Embed(
                title=title,
                description=content,
                color=discord.Color.blue(),
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f"Posted by {interaction.user.name}")
            await interaction.channel.send(embed=embed)
            await interaction.response.send_message("Post created successfully!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error creating post: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

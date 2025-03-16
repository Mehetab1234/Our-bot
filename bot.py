import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
from utils.logger import setup_logger
from utils.config import load_config

# Setup logging
logger = setup_logger()

# Bot configuration
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix='!',  # Keep prefix for compatibility
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )

    async def setup_hook(self):
        # Load all cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f"Loaded extension: {filename}")
                except Exception as e:
                    logger.error(f'Failed to load extension {filename}: {str(e)}')

        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f'Synced {len(synced)} command(s)')
        except Exception as e:
            logger.error(f'Failed to sync commands: {str(e)}')

    async def on_ready(self):
        logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        auth_link = discord.utils.oauth_url(
            self.user.id,
            permissions=discord.Permissions(
                administrator=True  # For full functionality including ticket system
            ),
            scopes=['bot', 'applications.commands']  # Add applications.commands scope
        )
        logger.info(f'Invite URL: {auth_link}')
        await self.change_presence(activity=discord.Game(name="/help for commands"))

    @commands.command(name='invite', help='Get the bot invite link')
    async def invite(self, ctx):
        auth_link = discord.utils.oauth_url(
            self.user.id,
            permissions=discord.Permissions(
                administrator=True
            ),
            scopes=['bot', 'applications.commands']
        )
        embed = discord.Embed(
            title="Invite Bot",
            description=f"Click [here]({auth_link}) to invite the bot to your server!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command not found. Use /help to see available commands.")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            logger.error(f'Error in command {ctx.command}: {str(error)}')
            await ctx.send(f"An error occurred: {str(error)}")

def main():
    # Get token from environment variable
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error('No token found in environment variables')
        return

    bot = DiscordBot()
    bot.run(token)

if __name__ == '__main__':
    main()

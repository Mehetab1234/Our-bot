import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Format(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='code', description='Format text as code')
    @app_commands.describe(
        language='Programming language',
        code='The code to format'
    )
    async def code(self, interaction: discord.Interaction, language: str, code: str):
        formatted = f"```{language}\n{code}\n```"
        await interaction.response.send_message(formatted)

    @app_commands.command(name='quote', description='Format text as a quote')
    @app_commands.describe(text='The text to quote')
    async def quote(self, interaction: discord.Interaction, text: str):
        formatted = "\n".join(f"> {line}" for line in text.split("\n"))
        await interaction.response.send_message(formatted)

    @app_commands.command(name='spoiler', description='Mark text as a spoiler')
    @app_commands.describe(text='The text to mark as spoiler')
    async def spoiler(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f"||{text}||")

    @app_commands.command(name='emojify', description='Convert text to regional indicator emojis')
    @app_commands.describe(text='The text to convert')
    async def emojify(self, interaction: discord.Interaction, text: str):
        # Convert to lowercase and replace spaces
        text = text.lower()
        regional_indicators = {
            chr(ord('a') + i): chr(ord('🇦') + i)
            for i in range(26)
        }
        
        result = ""
        for char in text:
            if char.isalpha():
                result += regional_indicators.get(char, char) + " "
            elif char == " ":
                result += "  "
            else:
                result += char + " "
                
        await interaction.response.send_message(result.strip())

    @app_commands.command(name='reverse', description='Reverse text')
    @app_commands.describe(text='The text to reverse')
    async def reverse(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text[::-1])

async def setup(bot):
    await bot.add_cog(Format(bot))

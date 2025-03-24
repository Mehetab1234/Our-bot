import discord
import openai
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Dictionary to store AI channels per server
ai_channels = {}

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_ai_response(self, prompt: str) -> str:
        """Generates a response from OpenAI based on user input."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error: {e}")
            return "⚠️ AI is currently unavailable. Please try again later."

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return  # Ignore bot messages & DMs

        guild_id = message.guild.id
        ai_channel_id = ai_channels.get(guild_id)  # Get AI channel for this server

        # Only respond in the AI channel if set
        if ai_channel_id and message.channel.id != ai_channel_id:
            return

        response = self.get_ai_response(message.content)
        await message.channel.send(response)

    @app_commands.command(name="ask", description="Ask the AI a question")
    async def ask(self, interaction: discord.Interaction, question: str):
        response = self.get_ai_response(question)
        await interaction.response.send_message(response)

    @app_commands.command(name="ai-channel", description="Set the AI response channel (Admins Only)")
    @commands.has_permissions(administrator=True)  # Only allow admins
    async def set_ai_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        guild_id = interaction.guild.id

        if channel:
            ai_channels[guild_id] = channel.id
            await interaction.response.send_message(f"✅ AI will now respond only in {channel.mention}", ephemeral=True)
        else:
            ai_channels.pop(guild_id, None)  # Remove restriction
            await interaction.response.send_message("✅ AI will now respond in **all channels**", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AI(bot))

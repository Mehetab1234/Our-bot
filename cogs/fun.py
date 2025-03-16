import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='roll', description='Roll a dice')
    @app_commands.describe(sides='Number of sides on the dice (default: 6)')
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 2:
            await interaction.response.send_message("A dice must have at least 2 sides!", ephemeral=True)
            return
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 You rolled a {result}!")

    @app_commands.command(name='flip', description='Flip a coin')
    async def flip(self, interaction: discord.Interaction):
        result = random.choice(['Heads', 'Tails'])
        await interaction.response.send_message(f"🪙 The coin landed on: {result}!")

    @app_commands.command(name='choose', description='Choose between multiple options')
    @app_commands.describe(choices='Options to choose from (separate with commas)')
    async def choose(self, interaction: discord.Interaction, choices: str):
        options = [choice.strip() for choice in choices.split(',')]
        if len(options) < 2:
            await interaction.response.send_message("Please provide at least 2 options separated by commas!", ephemeral=True)
            return
        choice = random.choice(options)
        await interaction.response.send_message(f"🤔 I choose: {choice}")

    @app_commands.command(name='8ball', description='Ask the magic 8-ball a question')
    @app_commands.describe(question='The question to ask')
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "Without a doubt.", "You may rely on it.", "Yes, definitely.",
            "As I see it, yes.", "Most likely.", "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.", "Don't count on it.", 
            "My sources say no.", "Very doubtful."
        ]
        await interaction.response.send_message(f"🎱 Question: {question}\nAnswer: {random.choice(responses)}")

    @app_commands.command(name='rps', description='Play Rock, Paper, Scissors')
    @app_commands.describe(choice='Your choice: rock, paper, or scissors')
    @app_commands.choices(choice=[
        app_commands.Choice(name='Rock', value='rock'),
        app_commands.Choice(name='Paper', value='paper'),
        app_commands.Choice(name='Scissors', value='scissors')
    ])
    async def rps(self, interaction: discord.Interaction, choice: str):
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)
        
        # Create emojis for choices
        emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        
        # Determine winner
        if choice == bot_choice:
            result = "It's a tie!"
        elif (
            (choice == 'rock' and bot_choice == 'scissors') or
            (choice == 'paper' and bot_choice == 'rock') or
            (choice == 'scissors' and bot_choice == 'paper')
        ):
            result = "You win!"
        else:
            result = "I win!"
        
        await interaction.response.send_message(
            f"You chose: {emojis[choice]} {choice}\n"
            f"I chose: {emojis[bot_choice]} {bot_choice}\n"
            f"Result: {result}"
        )

async def setup(bot):
    await bot.add_cog(Fun(bot))

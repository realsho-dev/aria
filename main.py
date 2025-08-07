# main.py

import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Healthcheck
import healthcheck
healthcheck.start()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '.')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

intents = discord.Intents.default()
intents.members = True    # needed to fetch members by ID
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# REMOVE DEFAULT HELP
bot.remove_command('help')

async def load_cogs():
    for folder in ["moderation", "utility", "ai", "bot"]:
        cog_dir = os.path.join(os.path.dirname(__file__), folder)
        if not os.path.isdir(cog_dir):
            continue
        for file in os.listdir(cog_dir):
            if file.endswith('.py') and file != "__init__.py":
                await bot.load_extension(f"{folder}.{file[:-3]}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
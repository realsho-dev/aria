import discord
from discord.ext import tasks, commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Set the bot status once when bot is ready
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your commands"))

async def setup(bot):
    await bot.add_cog(Status(bot))

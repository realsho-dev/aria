import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.set_status())

    async def set_status(self):
        await self.bot.wait_until_ready()
        activity = discord.Activity(type=discord.ActivityType.listening, name="your commands.")
        await self.bot.change_presence(activity=activity)

async def setup(bot):
    await bot.add_cog(Status(bot))

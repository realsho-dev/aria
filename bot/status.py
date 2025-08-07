import discord
from discord.ext import tasks, commands
import random

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            "just here, making your day better",
            "lowkey the smartest bot around",
            "flirting with code and you",
            "serving sass and answers all day",
            "too cool to be just a bot",
            "spicing up your chat sessions",
            "your virtual vibe master",
            "chatting, charming, conquering",
            "here to steal your attention",
            "no filter, all fire responses"
        ]
        self.change_status.start()

    @tasks.loop(minutes=5)
    async def change_status(self):
        new_status = random.choice(self.statuses)
        await self.bot.change_presence(activity=discord.Game(name=new_status))

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))

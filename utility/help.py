from discord.ext import commands

@commands.command(name="help")
async def help_command(ctx):
    msg = (
        "**Available commands:**\n"
        "**ban**, **clearwarns**, **help** (shows this message), **hide**, **kick**, **lock**, **nuke**,\n"
        "**purge**, **role**, **si**, **steal**, **timeout**, **ui**, **unhide**, **unlock**,\n"
        "**warn**, **warnings**"
    )
    await ctx.send(msg)

async def setup(bot):
    bot.add_command(help_command)

from discord.ext import commands

<<<<<<< HEAD

=======
>>>>>>> 0e53a4baa62402938ae71eab72dcd07f0720e244
@commands.command(name="help")
async def help_command(ctx):
    msg = (
        "**Available commands:**\n"
        "**ban**, **clearwarns**, **help**, **hide**, **kick**, **lock**, **nuke**,\n"
        "**purge**, **role**, **si**, **steal**, **timeout**, **ui**, **unhide**, **unlock**,\n"
<<<<<<< HEAD
        "**warn**, **warnings**, **nick**, **aichannel**, **ask**"
    )
    await ctx.send(msg)


async def setup(bot):
    bot.add_command(help_command)

=======
        "**warn**, **warnings**"
    )
    await ctx.send(msg)

async def setup(bot):
    bot.add_command(help_command)
>>>>>>> 0e53a4baa62402938ae71eab72dcd07f0720e244

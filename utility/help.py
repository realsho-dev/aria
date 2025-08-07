
<<<<<<< HEAD
=======
@commands.command(name="help")
async def help_command(ctx):
    msg = (
        "**Available commands:**\n"
        "**ban**, **clearwarns**, **help**, **hide**, **kick**, **lock**, **nuke**,\n"
        "**purge**, **role**, **si**, **steal**, **timeout**, **ui**, **unhide**, **unlock**,\n"
        "**warn**, **warnings**, **nick**, **aichannel**, **ask**"
    )
    await ctx.send(msg)

async def setup(bot):
    bot.add_command(help_command)
>>>>>>> origin/main

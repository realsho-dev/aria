from discord.ext import commands

@commands.command(name="help")
async def help_command(ctx):
    """shows all available commands organized by category"""
    
    msg = (
        "**aria command list**\n\n"
        
        "**moderation:**\n"
        "`ban`, `kick`, `timeout`, `warn`, `clearwarns`, `warnings`,\n"
        "`purge`, `lock`, `unlock`, `hide`, `unhide`, `nuke`\n\n"
        
        "**utility:**\n"
        "`role`, `nick`, `si`, `ui`, `steal`, `av`, `banner`\n\n"
        
        "**ai features:**\n"
        "`ask`, `aichannel`, `chatinfo`, `clearchat`, `reset`\n"
        "*also responds to @mentions anywhere*\n\n"
        
        "prefix: `.` | developed by ayanokouji"
    )
    
    await ctx.send(msg)

async def setup(bot):
    bot.add_command(help_command)

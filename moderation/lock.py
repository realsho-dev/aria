import discord
from discord.ext import commands
import random 

@commands.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    overwrite = ch.overwrites_for(ctx.guild.default_role)

    # Check if already locked
    if overwrite.send_messages is False:
        messages = [
            f"**#{ch.name}** is already locked down, nothing new here.",
            f"hey, **#{ch.name}** is closed tight already, chill.",
            f"nope, **#{ch.name}** is locked up already, easy there.",
            f"already locked! **#{ch.name}** ain't letting anyone talk now."
        ]
        await ctx.send(random.choice(messages))
        return

    overwrite.send_messages = False
    await ch.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    messages = [
        f"locked **#{ch.name}**, silence is golden here now!",
        f"all quiet in **#{ch.name}**, locked tight for everyone.",
        f"**#{ch.name}** just got the lockdown treatment, no talking.",
        f"shhh! **#{ch.name}** is locked, no messages allowed now."
    ]
    await ctx.send(random.choice(messages))

@commands.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    overwrite = ch.overwrites_for(ctx.guild.default_role)
    
    # Check if already unlocked or send_messages isn't False explicitly
    if overwrite.send_messages is None or overwrite.send_messages is True:
        messages = [
            f"**#{ch.name}** is already wide open, no lock here.",
            f"can’t unlock what’s not locked, **#{ch.name}** is open!",
            f"**#{ch.name}** was free already, just chillin’ and talkin’.",
            f"all good, **#{ch.name}** lets everyone message as usual."
        ]
        await ctx.send(random.choice(messages))
        return

    overwrite.send_messages = True
    await ch.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    messages = [
        f"unlocked **#{ch.name}**, chatterboxes rejoice! 🎉",
        f"freed up **#{ch.name}** for everyone, talk away now.",
        f"**#{ch.name}** is back to normal, send messages freely.",
        f"lock’s off in **#{ch.name}**, let the talk resume!"
    ]
    await ctx.send(random.choice(messages))

@commands.command(name="hide")
@commands.has_permissions(manage_channels=True)
async def hide(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    overwrite = ch.overwrites_for(ctx.guild.default_role)

    if overwrite.view_channel is False:
        messages = [
            f"**#{ch.name}** is already hidden away, secret spot.",
            f"can’t hide what’s already invisible, **#{ch.name}** is gone!",
            f"**#{ch.name}** is gone from everyone’s eyes already.",
            f"already hidden! **#{ch.name}** is your little secret now."
        ]
        await ctx.send(random.choice(messages))
        return

    overwrite.view_channel = False
    await ch.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    messages = [
        f"hid **#{ch.name}** from prying eyes, shhhh...",
        f"**#{ch.name}** vanished for everyone else, your secret spot.",
        f"now invisible: **#{ch.name}** is hidden away from all.",
        f"gone from view! **#{ch.name}** is your sneak spot now."
    ]
    await ctx.send(random.choice(messages))

@commands.command(name="unhide")
@commands.has_permissions(manage_channels=True)
async def unhide(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    overwrite = ch.overwrites_for(ctx.guild.default_role)

    # Treat None or True as visible already
    if overwrite.view_channel is None or overwrite.view_channel is True:
        messages = [
            f"**#{ch.name}** is already in plain sight for everyone.",
            f"nothing to unhide, **#{ch.name}** is visible already.",
            f"**#{ch.name}** can already be seen, all good here.",
            f"open and visible! **#{ch.name}** wasn’t hidden anyway."
        ]
        await ctx.send(random.choice(messages))
        return

    overwrite.view_channel = True
    await ch.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    messages = [
        f"brought back **#{ch.name}** into the spotlights, enjoy!",
        f"unhid **#{ch.name}**, now everyone can look and lurk.",
        f"revealed **#{ch.name}** from shadows, welcome back folks!",
        f"unhidden and clear! **#{ch.name}** can be seen again."
    ]
    await ctx.send(random.choice(messages))


async def setup(bot):
    bot.add_command(lock)
    bot.add_command(unlock)
    bot.add_command(hide)
    bot.add_command(unhide)

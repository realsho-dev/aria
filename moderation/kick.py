import discord
from discord.ext import commands
import random

@commands.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, who=None, *, reason=None):
    if not who:
        messages = [
            "hey, tell me who to kick, don’t leave me hanging.",
            "you gotta say a name if you want someone kicked.",
            "i’m waiting on a name, who’s getting the boot today?",
            "empty kick command? you need to say who to kick.",
        ]
        await ctx.send(random.choice(messages))
        return

    guild = ctx.guild
    target = None

    # FIND USER: Only mention or user ID accepted
    if ctx.message.mentions:
        target = ctx.message.mentions[0]
    elif who.isdigit():
        try:
            user_id = int(who)
            target = guild.get_member(user_id)
        except ValueError:
            target = None

    if not target:
        messages = [
            "send me a mention or user id, otherwise i’m lost.",
            "can’t find that user, you must @mention or give id.",
            "nope, i only take user mentions or ids, try again.",
            "that’s not a mention or a valid id, try again."
        ]
        await ctx.send(random.choice(messages))
        return

    if target == ctx.author:
        messages = [
            "lol, you really wanna kick yourself? that’s not allowed.",
            "you can’t kick yourself, gotta pick someone else instead.",
            "nice try kicking yourself, but that’s not how this works.",
            "sorry, self-kicks aren’t a thing here, pick another."
        ]
        await ctx.send(random.choice(messages))
        return

    if target == guild.owner:
        messages = [
            "the server owner is untouchable, you can’t kick them.",
            "bosses don’t get kicked, the owner’s safe from this.",
            "can’t kick the owner, rules say no, sorry pal.",
            "nope, kicking the server owner isn’t allowed here, try again."
        ]
        await ctx.send(random.choice(messages))
        return

    if target == guild.me:
        messages = [
            "haha, try as you might, you can’t kick me.",
            "kicking me? nope, not today, try someone else please.",
            "i’m safe from kicks, gotta pick a human user.",
            "can’t kick myself, but i appreciate the effort, thanks."
        ]
        await ctx.send(random.choice(messages))
        return

    if target.top_role >= guild.me.top_role:
        messages = [
            "their role’s higher than mine, can’t pull off that kick.",
            "would love to kick, but their role outranks my own.",
            "can’t kick that user, their role is above mine here.",
            "sorry, role hierarchy says i can’t kick this user."
        ]
        await ctx.send(random.choice(messages))
        return

    try:
        await target.kick(reason=reason)

        kick_messages = [
            f"**{target.name}** just got kicked, moving on swiftly.",
            f"bye bye, **{target.name}** is outta here now.",
            f"**{target.name}** took an unexpected exit, that’s that.",
            f"gone and dusted: **{target.name}** kicked from server.",
            f"that’s a wrap for **{target.name}**, kicked clean.",
            f"**{target.name}** just left the building, no turns back."
        ]
        msg = random.choice(kick_messages)
        if reason:
            msg += f" (`{reason}`)"
        await ctx.send(msg)

    except discord.Forbidden:
        messages = [
            "bot’s rank too low or missing kick permissions here.",
            "i tried but lack permissions to kick this user.",
            "permission denied, i can’t kick that one, sorry.",
            "kick failed, bot doesn’t have required powers to do it."
        ]
        await ctx.send(random.choice(messages))
    except Exception:
        messages = [
            "something broke, couldn’t kick that user, try again later.",
            "oops, failed to kick user, something went wrong here.",
            "well that didn’t work, couldn’t remove the user today.",
            "error happened while kicking, gotta try again some other time."
        ]
        await ctx.send(random.choice(messages))

async def setup(bot):
    bot.add_command(kick)

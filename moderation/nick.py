import discord
from discord.ext import commands
import random

@commands.command(name='nick')
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, who=None, *, nickname=None):
    if not who or not nickname:
        messages = [
            "gimme who and what nickname, can’t just work with blanks.",
            "nick command needs both user and new nickname, try again.",
            "who's getting a name change? and... to what?",
            "can't do nicks with nothing, throw me a user and nickname.",
        ]
        await ctx.send(random.choice(messages))
        return

    guild = ctx.guild
    target = None

    # FIND USER: @mention or ID only
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
            "need a user mention or id, plain and simple.",
            "nope, that’s not a mention or valid id, try again.",
            "can’t find that user, only taking mentions or ids.",
            "send the right stuff—a mention or user id please.",
        ]
        await ctx.send(random.choice(messages))
        return

    if target == guild.owner:
        messages = [
            "can't change the owner’s name, kind of a big deal.",
            "owner nicks are locked, you know how it goes.",
            "nope, changing the owner’s nickname isn’t a thing.",
            "boss’ name stays as is, pick someone else."
        ]
        await ctx.send(random.choice(messages))
        return

    if target == ctx.me:
        messages = [
            "nah, not changing my own nickname, pick a user.",
            "i’m good, try setting a nickname for someone else.",
            "can’t rename myself, robots have rules.",
            "nice try, i’ll stay as i am!"
        ]
        await ctx.send(random.choice(messages))
        return

    if target.top_role >= guild.me.top_role and target != ctx.me:
        messages = [
            "their role beats mine, can’t change that nickname.",
            "rank game’s too strong, I can’t touch that nickname.",
            "role hierarchy blocks me, nickname denied.",
            "can’t rename this user, they're above my pay grade."
        ]
        await ctx.send(random.choice(messages))
        return

    try:
        await target.edit(nick=nickname)
        nick_messages = [
            f"done. **{target.display_name}** is now rocking a new name: **{nickname}**.",
            f"fresh identity unlocked for {target.mention}: **{nickname}**.",
            f"nickname switch: {target.mention} → **{nickname}**.",
            f"new vibes? {target.name} is now **{nickname}** here.",
        ]
        await ctx.send(random.choice(nick_messages))
    except discord.Forbidden:
        messages = [
            "no powers to set that nickname, bot’s role too low or lacks permission.",
            "bot’s missing nickname rights—can’t make the change.",
            "not high enough to change that nickname, sorry.",
            "permission denied: can’t do the nickname shuffle."
        ]
        await ctx.send(random.choice(messages))
    except Exception:
        messages = [
            "something broke, nickname didn’t update, try later.",
            "nickname change failed, chaos in the wires.",
            "well that flopped, couldn’t set the nickname now.",
            "error on nickname change, maybe next time."
        ]
        await ctx.send(random.choice(messages))

async def setup(bot):
    bot.add_command(nick)

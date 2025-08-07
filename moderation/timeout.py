import discord
from discord.ext import commands
from datetime import timedelta
import random

@commands.command(name='timeout')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, who=None, duration: str = None, *, reason=None):
    # Find member from mention or ID
    member = None
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
    elif who and who.isdigit():
        member = ctx.guild.get_member(int(who))
    if not member:
        await ctx.send(random.choice([
            "can't timeout, mention or user id only, not found.",
            "no user found, mention someone or use user id.",
            "invalid user – only @mention or id will work here.",
            "that user isn't here, or input was wrong format.",
        ]))
        return

    if member == ctx.author:
        await ctx.send(random.choice([
            "not allowed: you can't timeout yourself, pick another.",
            "timeout yourself? nah, that's not something i do.",
            "can't timeout your own account, try a different user.",
            "nope, self-timeout is not an option here.",
        ]))
        return

    if member == ctx.guild.owner:
        await ctx.send(random.choice([
            "server owner can't be timed out, move on.",
            "timeout on owner? impossible here, try next user.",
            "owner immune, try to timeout someone else now.",
            "can't timeout the big boss, rules don't allow that.",
        ]))
        return

    if member == ctx.guild.me:
        await ctx.send(random.choice([
            "can't timeout myself (bot), pick a real member.",
            "not gonna timeout the bot. Try another user, please.",
            "you want me to timeout myself? not happening.",
            "bot doesn't timeout itself, try a human user.",
        ]))
        return

    if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
        await ctx.send(random.choice([
            "role too high for you, can't timeout them.",
            "timeout failed: their role is bigger than yours.",
            "that user can't be timed out — role power problem.",
            "your role's lower, can't do timeout here.",
        ]))
        return

    # No duration input: Try to remove timeout
    if not duration:
        try:
            await member.timeout(None, reason=reason)
            await ctx.send(random.choice([
                f"timeout cleared for **{member.name}**, chat's open again.",
                f"**{member.name}** can talk now, timeout just ended.",
                f"timeout removed for **{member.name}**, back in chat.",
                f"all good, timeout lifted for **{member.name}**.",
            ]))
        except discord.Forbidden:
            await ctx.send(random.choice([
                "can't clear timeout, missing permissions or bot rank issue.",
                "failed to end timeout, bot not powerful enough here.",
                "bot permission's missing for untimeout, can't do it.",
                "timeout clear failed, bot needs higher role/permissions.",
            ]))
        except Exception:
            await ctx.send("something broke, couldn't clear timeout.")
        return

    # Parse duration: s/m/h/d
    try:
        unit = duration[-1].lower()
        value = int(duration[:-1])
        if unit == 's':
            delta = timedelta(seconds=value)
        elif unit == 'm':
            delta = timedelta(minutes=value)
        elif unit == 'h':
            delta = timedelta(hours=value)
        elif unit == 'd':
            delta = timedelta(days=value)
        else:
            raise ValueError()
    except Exception:
        await ctx.send("give time like '10s', '3m', '2h', '1d' at the end.")
        return

    if delta.total_seconds() > 28 * 24 * 3600:
        await ctx.send("timeout can't be more than 28 days.")
        return

    try:
        await member.timeout(delta, reason=reason)
        msg = random.choice([
            f"**{member.name}** is timed out for **{duration}**, shhh.",
            f"muted **{member.name}** for **{duration}**, can't chat now.",
            f"timeout set for **{member.name}** for **{duration}**.",
            f"**{member.name}** got silenced for **{duration}**, enjoy your break.",
        ])
        if reason:
            msg += f" (`{reason}`)"
        await ctx.send(msg)
    except discord.Forbidden:
        await ctx.send(random.choice([
            "can't timeout, bot lacks permission or needs higher role.",
            "timeout failed, bot needs stronger permission for that.",
            "permission missing for me to timeout that user.",
            "bot can't timeout, needs better role or powers.",
        ]))
    except Exception:
        await ctx.send("couldn't timeout, something went wrong inside Discord.")

async def setup(bot):
    bot.add_command(timeout)

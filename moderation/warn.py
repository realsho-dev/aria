import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import random

WARN_FILE = "warns.json"

def load_warns():
    if os.path.isfile(WARN_FILE):
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(warns):
    with open(WARN_FILE, "w") as f:
        json.dump(warns, f, indent=2)

@commands.command(name="warn")
@commands.has_permissions(kick_members=True)
async def warn(ctx, who=None, *, reason=None):
    if who is None or reason is None:
        await ctx.send(random.choice([
            "use .warn <user/id> <reason>, don’t skip stuff.",
            "missing something: .warn (mention/userid) (reason), try again.",
            "need both user and reason for warning, buddy.",
            "give user and reason, can’t warn with blanks!"
        ]))
        return

    # find target
    member = None
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
    elif who.isdigit():
        member = ctx.guild.get_member(int(who))
    if not member:
        await ctx.send(random.choice([
            "no user found, mention or id only, not names.",
            "can't warn, that's not a valid member here.",
            "i can’t find that user, try again with id or tag.",
            "user not found, only mention/id work."
        ]))
        return

    # disallow bots
    if member.bot:
        await ctx.send(random.choice([
            "bots don’t get warnings, only humans mess up here.",
            "trying to warn a bot? not possible, pick a person.",
            "can’t warn a bot, try again with a real user.",
            "bots are off-limits, only warn server members."
        ]))
        return

    # can't warn self
    if member == ctx.author:
        await ctx.send(random.choice([
            "can't warn yourself, pick someone else for that job.",
            "warning yourself makes no sense, pick another user.",
            "no self-warning here, try a different member.",
            "not allowed to warn yourself, buddy."
        ]))
        return

    # mods can warn admins, but not the owner or the bot itself
    if member == ctx.guild.owner or member == ctx.guild.me:
        await ctx.send(random.choice([
            "can't warn server owner or the bot itself.",
            "owner and bot can’t be warned, rules are simple.",
            "not allowed to warn the big boss or bot.",
            "that's off-limits, owner or bot can’t be warned."
        ]))
        return

    warns = load_warns()
    uid = str(member.id)
    server = str(ctx.guild.id)
    warns.setdefault(server, {})
    warns[server].setdefault(uid, [])

    # add warn
    warns[server][uid].append({
        "reason": reason,
        "time": datetime.utcnow().isoformat(),
        "by": ctx.author.id
    })
    save_warns(warns)

    reply = random.choice([
        f"**{member.name}** warned: {reason}",
        f"warn given to **{member.name}** for: {reason}",
        f"added a warning to **{member.name}** – reason: {reason}",
        f"**{member.name}** now has a new warning for: {reason}",
    ])
    await ctx.send(reply)

@commands.command(name="warnings")
async def warnings(ctx, who=None):
    member = None
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
    elif who and who.isdigit():
        member = ctx.guild.get_member(int(who))
    if not member:
        await ctx.send(random.choice([
            "need a mention or id. can’t show warnings like this.",
            "user not found. use mention or proper id only.",
            "give a real user id or mention to see warns.",
            "can only show warnings for actual members here."
        ]))
        return

    warns = load_warns()
    uid = str(member.id)
    server = str(ctx.guild.id)
    user_warns = warns.get(server, {}).get(uid, [])
    if not user_warns:
        await ctx.send(f"**{member.name}** has no warnings yet.")
        return

    # Build warnings list with date and mod's username (not mention)
    lines = [f"**{member.name}**’s warnings:"]
    for i, w in enumerate(user_warns, 1):
        # Parse warning time ISO format and format date nicely (e.g. 2024-08-07)
        warn_time = w.get("time")
        try:
            dt = datetime.fromisoformat(warn_time)
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            date_str = "unknown date"

        mod_id = w.get("by")
        mod_member = ctx.guild.get_member(mod_id) if mod_id else None
        mod_name = mod_member.name if mod_member else "unknown mod"

        # Compose line: index. reason (date), warned by mod_name
        line = f"{i}. {w['reason']} ({date_str}), warned by **{mod_name}**"
        lines.append(line)

    # Send as a single message, minimal and clean
    await ctx.send("\n".join(lines))

@commands.command(name="clearwarns")
@commands.has_permissions(manage_guild=True)
async def clearwarns(ctx, who=None):
    member = None
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
    elif who and who.isdigit():
        member = ctx.guild.get_member(int(who))
    if not member:
        await ctx.send(random.choice([
            "use a mention or user id to clear warns.",
            "can’t clear, user not found. id or mention only.",
            "show a member by id/mention for clearing warnings.",
            "need the real user to clear warns out."
        ]))
        return

    warns = load_warns()
    uid = str(member.id)
    server = str(ctx.guild.id)
    if warns.get(server, {}).pop(uid, None) is not None:
        save_warns(warns)
        await ctx.send(random.choice([
            f"all warnings gone for **{member.name}**, cleaned up.",
            f"**{member.name}**’s warnings cleared, fresh start now.",
            f"no more warnings left for **{member.name}** here.",
            f"wiped out all warns for **{member.name}**, easy."
        ]))
    else:
        await ctx.send(random.choice([
            f"**{member.name}** had no warnings to clear anyway.",
            f"nothing to clear, **{member.name}** had a clean record.",
            f"**{member.name}** is already free of any warnings.",
            f"no warnings found for **{member.name}**, nothing cleared."
        ]))

async def setup(bot):
    bot.add_command(warn)
    bot.add_command(warnings)
    bot.add_command(clearwarns)

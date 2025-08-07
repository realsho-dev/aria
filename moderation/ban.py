import discord
from discord.ext import commands
import random

@commands.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, who=None, *, reason=None):
    if not who:
        await ctx.send(random.choice([
            "say who to ban, don't leave it empty.",
            "gotta tell me who to ban, try again.",
            "no user given, i can't ban no one.",
            "type a mention or id, then i'll ban."
        ]))
        return

    guild = ctx.guild
    target = None
    user_id = None

    # Try mention or user id only
    if ctx.message.mentions:
        target = ctx.message.mentions[0]
        user_id = target.id
    elif who.isdigit():
        user_id = int(who)
        target = guild.get_member(user_id)
    else:
        target = None

    # unban if user is already banned and id is given
    if user_id is not None:
        try:
            ban_entry = await guild.fetch_ban(discord.Object(id=user_id))
            await guild.unban(ban_entry.user, reason=reason)
            msg = random.choice([
                f"**{ban_entry.user.name}** was banned, now unbanned like you wanted.",
                f"unbanned **{ban_entry.user.name}**, back in server life.",
                f"all good, **{ban_entry.user.name}** is unbanned now.",
                f"**{ban_entry.user.name}** is back, just got unbanned.",
            ])
            if reason:
                msg += f" (`{reason}`)"
            await ctx.send(msg)
            return
        except discord.NotFound:
            pass  # not banned, proceed to ban

    if not target:
        await ctx.send(random.choice([
            "mention or user id only, no name search here.",
            "that's not a valid id or mention, try again.",
            "can't ban, i just need user id or mention.",
            "no user found, only ids or mentions work for me.",
        ]))
        return

    # special condition checks
    if target == ctx.author:
        await ctx.send(random.choice([
            "nope, can't ban yourself, pick someone else easy.",
            "banning yourself? not gonna work, try again.",
            "you can't ban your own self, pick another user.",
            "self-ban is not a thing here, sorry guy.",
        ]))
        return

    if target == guild.owner:
        await ctx.send(random.choice([
            "can't ban the owner, they're immune here.",
            "bosses don't get banned, try another user now.",
            "owner's safe, pick someone else to ban.",
            "no way to ban the owner, gotta pick different.",
        ]))
        return

    if target == guild.me:
        await ctx.send(random.choice([
            "nope, can't ban myself, pick a member easy.",
            "bot can't ban itself, try someone else please.",
            "self-ban as bot not allowed, move on.",
            "i'm here to help, not to get banned.",
        ]))
        return

    if target.top_role >= guild.me.top_role:
        await ctx.send(random.choice([
            "their role's higher than mine, can't ban them.",
            "that user outranks me, banning not possible.",
            "my rank is too low, can't ban that user.",
            "can't ban, their role is above mine here.",
        ]))
        return

    try:
        await guild.ban(target, reason=reason, delete_message_days=0)
        msg = random.choice([
            f"**{target.name}** is banned, done quick.",
            f"banned **{target.name}**, that's it.",
            f"**{target.name}** is gone now.",
            f"sent **{target.name}** out, banned fast.",
            f"bye **{target.name}**, banned in style.",
        ])
        if reason:
            msg += f" (`{reason}`)"
        await ctx.send(msg)
    except discord.Forbidden:
        await ctx.send(random.choice([
            "bot has no ban power, fix permissions first.",
            "can't ban, missing permissions as bot.",
            "i need higher permissions to ban this user.",
            "ban failed, permissions too low for that user.",
        ]))
    except Exception:
        await ctx.send(random.choice([
            "couldn't ban, something broke, maybe try again.",
            "failed to ban user, not sure what's wrong.",
            "error on ban, try again or check stuff.",
            "ban didn't work, maybe check bot roles again.",
        ]))

async def setup(bot):
    bot.add_command(ban)

import discord
from discord.ext import commands
import asyncio
import random

@commands.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx, channel: discord.TextChannel = None):
    ch = channel or ctx.channel
    confirm_msgs = [
        f"about to nuke **#{ch.name}** — reply yes/yep/yess/yus quick (5s)!",
        f"ready to nuke **#{ch.name}**? type a wild yes/yup/yss now (5s)!",
        f"warning! reply yes/yep/yup/yss/yus to nuke **#{ch.name}** in 5s.",
        f"final call: reply yes, yep, yus etc in 5s to nuke **#{ch.name}**."
    ]
    confirm = await ctx.send(random.choice(confirm_msgs))

    def check(m):
        return (
            m.author.id == ctx.author.id
            and m.channel.id == ctx.channel.id
            and any(x in m.content.lower().replace(" ", "") for x in ["yes","yep","yup","yus","yss"])
        )
    try:
        reply = await ctx.bot.wait_for('message', timeout=5, check=check)
        nukelines = [
            f"boom. nuked **#{ch.name}**, made a fresh one right here.",
            f"channel nuked: **#{ch.name}** reset, all messages wiped.",
            f"smashed and rebuilt **#{ch.name}** in the same spot.",
            f"bye old stuff, **#{ch.name}** wiped, brand new now."
        ]
        # Save data before delete
        name = ch.name
        pos = ch.position
        perm = ch.overwrites
        topic = ch.topic
        slow = ch.slowmode_delay
        nsfw = getattr(ch, 'nsfw', False)
        category = ch.category

        await ch.delete()
        newch = await ctx.guild.create_text_channel(
            name=name,
            position=pos,
            category=category,
            overwrites=perm,
            topic=topic,
            slowmode_delay=slow,
            nsfw=nsfw,
            reason="Nuke command"
        )
        await newch.send(random.choice(nukelines))
    except asyncio.TimeoutError:
        messages = [
            "no confirmation — nuke cancelled, nothing deleted here.",
            "time up — missed it, not nuking anything today.",
            "not confirmed in 5s, so nothing wiped out.",
            "missed your chance — channel stays as is for now."
        ]
        try: await confirm.delete()
        except: pass
        await ctx.send(random.choice(messages), delete_after=2)

async def setup(bot):
    bot.add_command(nuke)

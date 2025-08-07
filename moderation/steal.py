import discord
from discord.ext import commands
import aiohttp
import re
import random

def random_emoji_name():
    return f"emoji-{random.randint(1000,9999)}"

async def unique_emoji_name(guild, base):
    name = base
    i = 1
    while any(e.name == name for e in guild.emojis):
        name = f"{base}-{i}"
        i += 1
    return name

@commands.command(name="steal")
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, arg=None):
    # 1. Reply to custom emoji
    if ctx.message.reference:
        refmsg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        # Try extracting emoji from message content
        matches = re.findall(r'<a?:([a-zA-Z0-9_]+):([0-9]+)>', refmsg.content)
        # If nothing in content, check attachments (for emoji from image)
        if not matches and refmsg.attachments:
            img = refmsg.attachments[0]
            emname = (arg or img.filename.split('.')[0] or random_emoji_name()).lower()
            emname = await unique_emoji_name(ctx.guild, emname)
            data = await img.read()
            try:
                emoji = await ctx.guild.create_custom_emoji(name=emname, image=data, reason=f"Steal by {ctx.author}")
                await ctx.send(f"added emoji **{emoji.name}** from image. all set.")
            except discord.Forbidden:
                await ctx.send("no perms to add emoji, check bot role perms.")
            except Exception:
                await ctx.send("couldn’t add emoji, maybe slot is full or server error.")
            return

        if not matches:
            await ctx.send(random.choice([
                "couldn’t find emoji to steal, reply to a real emoji.",
                "no custom emoji found, send a message with it please.",
                "emoji missing from target, try another one next time.",
                "no usable emoji in that message, give me a real one."
            ])); return

        # Use the first found emoji
        ename, eid = matches[0]
        emoji_url = f"https://cdn.discordapp.com/emojis/{eid}.{'gif' if refmsg.content.startswith('<a:') else 'png'}"
        emname = (arg or ename or random_emoji_name()).lower()
        emname = await unique_emoji_name(ctx.guild, emname)
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as r:
                if r.status != 200:
                    await ctx.send("couldn’t download the emoji, check network or emoji deleted.")
                    return
                data = await r.read()
        try:
            emoji = await ctx.guild.create_custom_emoji(name=emname, image=data, reason=f"Steal by {ctx.author}")
            await ctx.send(random.choice([
                f"stolen and named **{emoji.name}**, that’s done.",
                f"emoji added as **{emoji.name}**, mission complete.",
                f"all good, new emoji: **{emoji.name}** is live.",
                f"uploaded as **{emoji.name}**, enjoy your new emoji."
            ]))
        except discord.Forbidden:
            await ctx.send("not allowed to add emoji — perms missing.")
        except Exception:
            await ctx.send("something broke adding this emoji, maybe slot full.")
        return

    # 2. .steal <image_url>
    if arg and (arg.startswith("http://") or arg.startswith("https://")):
        img_url = arg
        emname = random_emoji_name()
        async with aiohttp.ClientSession() as session:
            async with session.get(img_url) as r:
                if r.status != 200 or not r.headers.get('Content-Type','').startswith("image/"):
                    await ctx.send("that does not look like a valid image URL.")
                    return
                data = await r.read()
        final_name = await unique_emoji_name(ctx.guild, emname)
        try:
            emoji = await ctx.guild.create_custom_emoji(name=final_name, image=data, reason=f"Steal from URL by {ctx.author}")
            await ctx.send(f"emoji created from url as **{emoji.name}**, saved.")
        except discord.Forbidden:
            await ctx.send("missing permission, can’t add emoji here.")
        except Exception:
            await ctx.send("couldn’t add from url image, error or slot full.")
        return

    await ctx.send("reply to an emoji/msg or give image link only.")

async def setup(bot):
    bot.add_command(steal)

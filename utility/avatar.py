import discord
from discord.ext import commands
import random

@commands.command(name="avatar", aliases=["av"])
async def avatar(ctx, user: discord.Member = None):
    target = user or ctx.author

    if user is None:
        # No user given, just show author’s avatar
        embed = discord.Embed(title=f"avatar for **{target.name}**", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        await ctx.send(embed=embed)
        return

    # User specified - check if member valid
    if not target:
        msgs = [
            "can’t find that user, check the id or mention again.",
            "hmm, no user exists with that id or mention here.",
            "user missing, try tagging or putting a valid user id.",
            "no user found for that input, gimme a valid mention/id.",
        ]
        await ctx.send(random.choice(msgs))
        return

    # Optional: Special messages for bots
    if target.bot:
        msgs = [
            "here’s the bot’s avatar for you, all robot vibes!",
            "bot avatar coming right up, no humans this time!",
            "bot detected, but avatar’s just the same, enjoy!",
            "machines have faces too — here’s this bot’s avatar!"
        ]
        embed = discord.Embed(title=f"avatar for **{target.name}** (bot)", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        await ctx.send(random.choice(msgs), embed=embed)
        return

    # Normal user avatar display
    try:
        embed = discord.Embed(title=f"avatar for **{target.name}**", color=discord.Color.blue())
        embed.set_image(url=target.display_avatar.url)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(random.choice([
            "oops, failed to get avatar, try again later please.",
            "something went wrong, can’t fetch that avatar right now.",
            "error fetching avatar, maybe retry or check the user?",
            "whoops, ran into trouble grabbing avatar, try later."
        ]))

async def setup(bot):
    bot.add_command(avatar)

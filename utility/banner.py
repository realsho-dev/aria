import discord
from discord.ext import commands
import random

@commands.command(name="banner", aliases=["bn"])
async def banner(ctx, user: discord.User = None):
    target = user or ctx.author

    try:
        # Fetch full user to get banner
        fetched_user = await ctx.bot.fetch_user(target.id)
    except Exception:
        await ctx.send("failed to fetch user data, try again later.")
        return

    # No banner case
    if not fetched_user.banner:
        msgs = [
            "this user doesn’t have a banner set.",
            "no banner found here, looks empty.",
            "banner missing, nothing to show.",
            "this profile has no banner yet."
        ]
        await ctx.send(random.choice(msgs))
        return

    # Bot banner
    if fetched_user.bot:
        msgs = [
            "bot banner detected, robotic aesthetics!",
            "here’s the bot’s banner, machines got style too!",
            "bot profile banner coming right up!",
            "no humans, just a bot banner 😄"
        ]
        embed = discord.Embed(
            title=f"banner for **{fetched_user.name}** (bot)",
            color=discord.Color.blue()
        )
        embed.set_image(url=fetched_user.banner.url)
        await ctx.send(random.choice(msgs), embed=embed)
        return

    # Normal user banner
    try:
        embed = discord.Embed(
            title=f"banner for **{fetched_user.name}**",
            color=discord.Color.blue()
        )
        embed.set_image(url=fetched_user.banner.url)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(random.choice([
            "oops, failed to get banner, try again later.",
            "something went wrong while fetching the banner.",
            "error grabbing banner, maybe retry?",
            "whoops, banner extraction failed."
        ]))


async def setup(bot):
    bot.add_command(banner)

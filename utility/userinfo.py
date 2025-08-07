import discord
from discord.ext import commands
import random
from datetime import datetime

@commands.command(name="ui")
async def userinfo(ctx, user: discord.Member = None):
    target = user or ctx.author
    guild = ctx.guild

    # If user supplied but not found (should not happen with discord.Member converter)
    if target is None:
        fallback_replies = [
            "who? no user found, try mention or valid id.",
            "can’t find that user here, check your input again.",
            "no such member in this server, try tagging them.",
            "user missing, make sure you mention or give the right id."
        ]
        await ctx.send(random.choice(fallback_replies))
        return

    # Start assembling embed
    embed = discord.Embed(title=f"User info for **{target.name}#{target.discriminator}**",
                          color=discord.Color.blurple(),
                          timestamp=datetime.utcnow())

    embed.set_thumbnail(url=target.display_avatar.url)

    # Fields (try 12 fields)
    fields = [
        ("User ID", f"**{target.id}**"),
        ("Bot?", "**Yes**" if target.bot else "**No**"),
        ("Created at", target.created_at.strftime("**%Y-%m-%d %H:%M UTC**")),
        ("Joined server", target.joined_at.strftime("**%Y-%m-%d %H:%M UTC**") if target.joined_at else "Never joined?"),
        ("Top role", f"**{target.top_role.name}**" if target.top_role else "No roles"),
        ("Roles count", f"**{len(target.roles) - 1}** (excluding @everyone)"),
        ("Nickname", f"**{target.nick}**" if target.nick else "No nickname"),
        ("User status", f"**{str(target.status).title()}**"),
        ("Activity", f"**{str(target.activity.name) if target.activity else 'None'}**"),
        ("Mention", f"{target.mention}"),
        ("Accent color", f"#{str(target.accent_color.value)[2:].upper()}" if target.accent_color else "None"),
        ("Is server owner?", "**Yes**" if target == guild.owner else "**No**"),
        ("Is premium booster?", "**Yes**" if target.premium_since else "**No**"),
    ]

    for name, value in fields:
        embed.add_field(name=name, value=value, inline=True)

    # Unique informal footer
    footers = [
        "User info served with style and minimal fuss.",
        "Looking sharp with all that info, enjoy!",
        "That’s the scoop on this user, neat huh?",
        "All the essentials, nice and tidy for you."
    ]
    embed.set_footer(text=random.choice(footers))

    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(userinfo)

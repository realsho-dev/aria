import discord
from discord.ext import commands
import random
from datetime import datetime

@commands.command(name="si")
async def serverinfo(ctx):
    guild = ctx.guild

    embed = discord.Embed(
        title=f"server info for **{guild.name}**",
        color=discord.Color.blurple(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)

    embed.add_field(name="ID", value=f"**{guild.id}**", inline=True)
    embed.add_field(name="Owner", value=f"**{guild.owner.name if guild.owner else 'Unknown'}**", inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("**%Y-%m-%d %H:%M UTC**"), inline=True)
    embed.add_field(name="Members", value=f"**{guild.member_count}**", inline=True)
    embed.add_field(name="Humans", value=f"**{sum(not m.bot for m in guild.members)}**", inline=True)
    embed.add_field(name="Bots", value=f"**{sum(m.bot for m in guild.members)}**", inline=True)
    embed.add_field(name="Channels", value=f"**{len(guild.text_channels) + len(guild.voice_channels)}**", inline=True)
    embed.add_field(name="Text", value=f"**{len(guild.text_channels)}**", inline=True)
    embed.add_field(name="Voice", value=f"**{len(guild.voice_channels)}**", inline=True)
    embed.add_field(name="Roles", value=f"**{len(guild.roles)-1}**", inline=True)
    embed.add_field(name="Emojis", value=f"**{len(guild.emojis)}**", inline=True)
    embed.add_field(name="Boosts", value=f"**{guild.premium_subscription_count or 0}**", inline=True)
    embed.add_field(name="Level", value=f"**{guild.premium_tier}**", inline=True)
    embed.add_field(name="AFK channel", value=f"**{guild.afk_channel.name if guild.afk_channel else 'No afk'}**", inline=True)
    embed.set_footer(text=random.choice([
        "just the important server details, nothing extra.",
        "everything you need to know about the server here.",
        "here’s your server info, all neat and tidy."
    ]))

    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(serverinfo)

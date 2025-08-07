import discord
from discord.ext import commands
import random
from difflib import get_close_matches

def find_role(guild, search):
    # Exact ID
    if search.isdigit():
        role = discord.utils.get(guild.roles, id=int(search))
        if role: return role
    # Exact name
    for r in guild.roles:
        if r.name.lower() == search.lower():
            return r
    # Fuzzy name
    names = [r.name.lower() for r in guild.roles]
    match = get_close_matches(search.lower(), names, n=1, cutoff=0.6)
    if match:
        return discord.utils.get(guild.roles, name=match[0])
    return None

@commands.command(name='role')
@commands.has_permissions(manage_roles=True)
async def role(ctx, target=None, *, role_input=None):
    if target is None or role_input is None:
        await ctx.send(random.choice([
            "say someone/all/humans/bots and a role. don’t leave blank.",
            "put user/id/group and role too, not just one.",
            "missing either the user/group or the role, can’t go on.",
            "usage: .role (user/id/all/bots/humans) (role name/id)"
        ])); return

    guild = ctx.guild
    role = find_role(guild, role_input)
    if not role:
        await ctx.send(random.choice([
            f"no role like **{role_input}** found here, check spelling.",
            f"can’t find role **{role_input}**, try a real one.",
            f"missing that role: **{role_input}** in the server.",
            f"nothing named **{role_input}** in roles, try another."
        ])); return

    # Group targets
    lower_target = target.lower()
    if lower_target in ["all", "humans", "bots"]:
        members = guild.members if lower_target == "all" else (
            [m for m in guild.members if not m.bot] if lower_target == "humans" else [m for m in guild.members if m.bot]
        )
        add_count, rem_count = 0, 0
        for m in members:
            try:
                if role in m.roles:
                    await m.remove_roles(role, reason=f"Role by {ctx.author}")
                    rem_count += 1
                else:
                    await m.add_roles(role, reason=f"Role by {ctx.author}")
                    add_count += 1
            except:
                pass
        if add_count and rem_count:
            msg = f"added **{role.name}** to {add_count}, removed from {rem_count}."
        elif add_count:
            msg = random.choice([
                f"every target now got **{role.name}**, all upgraded.",
                f"added **{role.name}** for {add_count} users, nice.",
                f"mass assignment: everyone owns **{role.name}** role!", 
                f"gave **{role.name}** everywhere, now that’s team spirit."
            ])
        elif rem_count:
            msg = random.choice([
                f"wiped **{role.name}** from {rem_count} users, all gone.",
                f"all had **{role.name}** and now it’s removed.",
                f"removed **{role.name}** for everyone this round.",
                f"cleaned all **{role.name}** holders, looking tidy."
            ])
        else:
            msg = "failed to change any roles, bot likely lacks permissions."
        await ctx.send(msg)
        return

    # Single user
    member = ctx.message.mentions[0] if ctx.message.mentions else (
        guild.get_member(int(target)) if target.isdigit() else None
    )
    if not member:
        await ctx.send(random.choice([
            "only mention/id for user, that one’s not found.",
            "can’t find user with that id or mention.",
            "no such person here, try again with mention or id.",
            "that user is missing, use correct id or mention."
        ])); return
    if member.bot:
        await ctx.send(random.choice([
            "leaving bots alone, skip role toggle for bots.",
            "won’t change roles for bots, only for people.",
            "bots keep their own setup, humans only.",
            "nothing to toggle for bots here, buddy."
        ])); return

    try:
        if role in member.roles:
            await member.remove_roles(role, reason=f"Role by {ctx.author}")
            msg = random.choice([
                f"took **{role.name}** off **{member.name}**, no more.",
                f"removed **{role.name}** for **{member.name}**, all clean.",
                f"stripped away **{role.name}** from **{member.name}**.",
                f"bye to **{role.name}** from **{member.name}**."
            ])
        else:
            await member.add_roles(role, reason=f"Role by {ctx.author}")
            msg = random.choice([
                f"gave **{role.name}** to **{member.name}**, fresh look.",
                f"**{member.name}** upgraded with **{role.name}** role.",
                f"just added **{role.name}** to **{member.name}**.",
                f"**{member.name}** wins new **{role.name}** role, nice."
            ])
        await ctx.send(msg)
    except discord.Forbidden:
        await ctx.send("not enough power to change roles here, fix perms.")
    except Exception:
        await ctx.send("something broke when toggling role, maybe permissions.")

async def setup(bot):
    bot.add_command(role)

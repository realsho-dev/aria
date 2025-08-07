import discord
from discord.ext import commands
import asyncio

@commands.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, arg1=None, arg2=None):
    channel = ctx.channel

    def is_human(msg): return not msg.author.bot
    def is_bot(msg): return msg.author.bot
    def is_user(user): return lambda m: m.author.id == user.id

    # Helper for temp message with auto-delete
    async def tempmsg(content):
        msg = await ctx.send(content)
        await asyncio.sleep(5)
        try: await msg.delete()
        except: pass

    # .purge all
    if arg1 and arg1.lower() == "all":
        deleted = await channel.purge(check=lambda m: True)
        await tempmsg(f"all messages gone, cleaned everything here in a flash.")

    # .purge bots 7 or .purge bots
    elif arg1 and arg1.lower() == "bots":
        limit = int(arg2) if arg2 and arg2.isdigit() else None
        if limit:
            deleted = await channel.purge(limit=2000, check=is_bot)
            deleted = deleted[:limit]
            for m in deleted:
                await m.delete()
            await tempmsg(f"cleared last {limit} bot messages, nice and tidy now.")
        else:
            deleted = await channel.purge(check=is_bot)
            await tempmsg(f"wiped out every bot message here, done quick.")

    # .purge humans 5 or .purge humans
    elif arg1 and arg1.lower() == "humans":
        limit = int(arg2) if arg2 and arg2.isdigit() else None
        if limit:
            deleted = []
            async for msg in channel.history(limit=2000):
                if is_human(msg):
                    deleted.append(msg)
                    if len(deleted) == limit:
                        break
            for m in deleted:
                await m.delete()
            await tempmsg(f"cleaned last {limit} human messages, neat now.")
        else:
            deleted = await channel.purge(check=is_human)
            await tempmsg(f"all human messages zapped, nothing left for now.")

    # .purge @user/id <n> or .purge @user/id
    elif arg1:
        user = None
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        elif arg1.isdigit():
            user = ctx.guild.get_member(int(arg1))
        if user:
            if arg2 and arg2.isdigit():
                limit = int(arg2)
                msgs = []
                async for msg in channel.history(limit=2000):
                    if msg.author.id == user.id:
                        msgs.append(msg)
                        if len(msgs) == limit:
                            break
                for m in msgs:
                    await m.delete()
                await tempmsg(f"cleared {limit} recent messages from **{user.name}** fast.")
            else:
                deleted = await channel.purge(check=is_user(user))
                await tempmsg(f"all messages by **{user.name}** erased from channel.")
            return

        # .purge n
        if arg1.isdigit():
            n = int(arg1)
            deleted = await channel.purge(limit=n+1)
            await tempmsg(f"cleared last {n} messages plus my own too.")
            return

        # fallback
        await tempmsg("not sure what to do, check your command again.")
    else:
        await tempmsg("say what and how much to purge, don't leave blank.")

async def setup(bot):
    bot.add_command(purge)

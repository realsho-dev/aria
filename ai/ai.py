import os
import textwrap
from dotenv import load_dotenv
from together import Together
from discord.ext import commands
import discord

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
BOT_PREFIX = '.'

# ==================== UPDATED ARIA PROMPT ====================

def format_system_prompt(): 
    return textwrap.dedent(""" 
    About Yourself: 
    1. You are aria, a helpful AI discord bot. 
    2. You can answer questions, provide info, and assist with tasks. 
    3. You are friendly, very short, and highly informal. 
    4. You are developed by Ayanokouji. 
    Response Rules: 
    1. Be very short but helpful (10-15 words with lower case only, and informal tone) 
    2. Use conversation history to maintain context and continuity 
    3. Reply naturally with informal style 
    """).strip()


# ==================== TOKEN ESTIMATION ====================

def count_tokens_estimate(messages):
    total = sum(len(msg["content"]) for msg in messages)
    return total // 4


# ==================== MAIN COG ====================

class AICommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled_channels = set()
        self.chat_history = {}
        self.max_tokens = 2000
        self.max_messages = 20

    def add_to_history(self, user_id, role, content):
        if user_id not in self.chat_history:
            self.chat_history[user_id] = []
        self.chat_history[user_id].append({"role": role, "content": content})

        while count_tokens_estimate(self.chat_history[user_id]) > self.max_tokens:
            if len(self.chat_history[user_id]) > 1:
                self.chat_history[user_id].pop(0)
            else:
                break

        if len(self.chat_history[user_id]) > self.max_messages:
            self.chat_history[user_id] = self.chat_history[user_id][-self.max_messages:]

    def get_history(self, user_id):
        return self.chat_history.get(user_id, [])

    def get_ai_response_with_history(self, user_id, prompt):
        try:
            system_prompt = format_system_prompt()
            messages = [{"role": "system", "content": system_prompt}]
            history = self.get_history(user_id)
            messages.extend(history)
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model="meta-llama/Llama-3-70b-chat-hf",
                messages=messages,
                temperature=0.6,
                max_tokens=220,
                top_p=0.9,
            )

            ai_reply = response.choices[0].message.content.strip()

            self.add_to_history(user_id, "user", prompt)
            self.add_to_history(user_id, "assistant", ai_reply)
            return ai_reply

        except Exception as e:
            print(f"AI Error: {e}")
            return "uhh something glitched lol..."

    # ==================== ASK COMMAND ====================

    @commands.command(name="ask")
    async def handle_ask_command(self, ctx, *, prompt: str):
        extra_context = None
        if ctx.message.reference:
            try:
                ref_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                extra_context = f"[Replying to: {ref_msg.content}]\n\n"
            except Exception as e:
                print(f"Couldn't fetch replied message: {e}")

        full_prompt = (extra_context + prompt) if extra_context else prompt

        reply = await self.bot.loop.run_in_executor(
            None,
            self.get_ai_response_with_history,
            ctx.author.id,
            full_prompt,
        )
        await ctx.send(reply)

    # ==================== AI CHANNEL FEATURE ====================

    @commands.command(name="aichannel")
    @commands.has_permissions(manage_channels=True)
    async def aichannel(self, ctx, *, channel_id=None):
        channel = None
        if channel_id:
            try:
                channel = self.bot.get_channel(int(channel_id))
            except Exception:
                channel = None
        if not channel:
            channel = ctx.channel

        if channel.id in self.enabled_channels:
            self.enabled_channels.remove(channel.id)
            await ctx.send(f"aichat disabled in {channel.mention}")
        else:
            self.enabled_channels.add(channel.id)
            await ctx.send(f"aichat enabled in {channel.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(BOT_PREFIX):
            return

        bot_mentioned = self.bot.user in message.mentions
        in_enabled_channel = message.channel.id in self.enabled_channels

        if not (bot_mentioned or in_enabled_channel):
            return

        prompt = message.content
        if bot_mentioned:
            prompt = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            prompt = prompt.replace(f'<@!{self.bot.user.id}>', '').strip()

        reply_text = await self.bot.loop.run_in_executor(
            None,
            self.get_ai_response_with_history,
            message.author.id,
            prompt,
        )

        if bot_mentioned:
            await message.reply(reply_text, mention_author=False)
        else:
            await message.channel.send(reply_text)

    # ==================== HISTORY MANAGEMENT ====================

    @commands.command(name="clearchat")
    async def clearchat(self, ctx):
        user_id = ctx.author.id
        if user_id in self.chat_history:
            del self.chat_history[user_id]
            await ctx.send("ur chat history’s gone lol")
        else:
            await ctx.send("no history found...")

    @commands.command(name="chatinfo")
    async def chatinfo(self, ctx):
        user_id = ctx.author.id
        if user_id in self.chat_history:
            msg_count = len(self.chat_history[user_id])
            token_count = count_tokens_estimate(self.chat_history[user_id])
            await ctx.send(f"msgs: {msg_count} | est tokens: {token_count}")
        else:
            await ctx.send("no history found...")

    @commands.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        total_users = len(self.chat_history)
        total_channels = len(self.enabled_channels)
        self.chat_history.clear()
        self.enabled_channels.clear()
        await ctx.send(
            f"✅ **bot reset done**\n"
            f"• cleared history for {total_users} users\n"
            f"• disabled {total_channels} ai channels"
        )

    @commands.command(name="clearask")
    async def clear_ask_history(self, ctx):
        await self.clearchat(ctx)

    @commands.command(name="askinfo")
    async def ask_info(self, ctx):
        await self.chatinfo(ctx)


async def setup(bot):
    await bot.add_cog(AICommandsCog(bot))

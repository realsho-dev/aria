import os
import textwrap
from dotenv import load_dotenv
from together import Together
from discord.ext import commands

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
BOT_PREFIX = '.'

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

def count_tokens_estimate(messages):
    """rough token estimation: ~4 chars = 1 token"""
    total = sum(len(msg["content"]) for msg in messages)
    return total // 4

def get_ai_response_with_history(user_id, prompt, cog_instance):
    try:
        system_prompt = format_system_prompt()
        
        # build message list: system + history + current
        messages = [{"role": "system", "content": system_prompt}]
        
        # add stored history
        history = cog_instance.get_history(user_id)
        messages.extend(history)
        
        # add current message
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=messages,
            temperature=0.7,
            max_tokens=100,
        )
        
        ai_reply = response.choices[0].message.content.strip()
        
        # save to history
        cog_instance.add_to_history(user_id, "user", prompt)
        cog_instance.add_to_history(user_id, "assistant", ai_reply)
        
        return ai_reply
    except Exception as e:
        print(f"AI Error: {e}")
        return "oops something broke lol"

class AIChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled_channels = set()
        self.chat_history = {}  # user_id -> list of messages
        self.max_tokens = 2000  # token limit per user
        self.max_messages = 20  # fallback message limit

    def add_to_history(self, user_id, role, content):
        """add message to history with token management"""
        if user_id not in self.chat_history:
            self.chat_history[user_id] = []
        
        self.chat_history[user_id].append({"role": role, "content": content})
        
        # remove oldest messages if exceeding token limit
        while count_tokens_estimate(self.chat_history[user_id]) > self.max_tokens:
            if len(self.chat_history[user_id]) > 1:
                self.chat_history[user_id].pop(0)
            else:
                break
        
        # also enforce message count limit
        if len(self.chat_history[user_id]) > self.max_messages:
            self.chat_history[user_id] = self.chat_history[user_id][-self.max_messages:]
    
    def get_history(self, user_id):
        """get conversation history for user"""
        return self.chat_history.get(user_id, [])

    @commands.command(name="aichannel")
    async def aichannel(self, ctx, *, channel_id=None):
        """toggle AI chat in a channel"""
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

    @commands.command(name="clearchat")
    async def clearchat(self, ctx):
        """clear your conversation history"""
        user_id = ctx.author.id
        if user_id in self.chat_history:
            del self.chat_history[user_id]
            await ctx.send("your chat history cleared!")
        else:
            await ctx.send("no history found")

    @commands.command(name="chatinfo")
    async def chatinfo(self, ctx):
        """show your chat history stats"""
        user_id = ctx.author.id
        if user_id in self.chat_history:
            msg_count = len(self.chat_history[user_id])
            token_count = count_tokens_estimate(self.chat_history[user_id])
            await ctx.send(f"messages stored: {msg_count} | estimated tokens: {token_count}")
        else:
            await ctx.send("no history found")

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore if not in enabled channel
        if message.channel.id not in self.enabled_channels:
            return
        
        # ignore bot messages
        if message.author.bot:
            return
        
        # ignore commands
        if message.content.startswith(BOT_PREFIX):
            return

        # get AI response with full history
        reply_text = get_ai_response_with_history(
            message.author.id, 
            message.content, 
            self
        )
        await message.channel.send(reply_text)

async def setup(bot):
    await bot.add_cog(AIChannelCog(bot))

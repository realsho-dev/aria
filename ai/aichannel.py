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
        2. Do not use past chat, focus only on current prompt
        3. Reply naturally with informal style
    """).strip()

def get_ai_response(prompt):
    try:
        system_prompt = format_system_prompt()
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "oops something broke lol"

class AIChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled_channels = set()

    @commands.command(name="aichannel")
    async def aichannel(self, ctx, *, channel_id=None):
        # Enable/disable AI in a channel
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
        # Only reply if channel is enabled and not a bot
        if message.channel.id not in self.enabled_channels:
            return
        if message.author.bot:
            return
        if message.content.startswith(BOT_PREFIX):
            return  # ignore .commands

        # Get AI response and send
        reply = get_ai_response(message.content)
        await message.channel.send(reply)

async def setup(bot):
    await bot.add_cog(AIChannelCog(bot))

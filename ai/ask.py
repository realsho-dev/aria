import os
import textwrap
from dotenv import load_dotenv
from together import Together
from discord.ext import commands

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
BOT_PREFIX = '-'

def format_system_prompt():
    return textwrap.dedent(f"""
        About Yourself:
        1. You are aria, a helpful AI assistant.
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
                # Removed assistant context (no history now)
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100,  # reduced since no history and short replies expected
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "oops something broke lol"

# Register as a Discord command
@commands.command(name="ask")
async def handle_ask_command(ctx, *, prompt: str):
    reply = get_ai_response(prompt)
    await ctx.send(reply)

# Required for Discord.py extension loading
async def setup(bot):
    bot.add_command(handle_ask_command)
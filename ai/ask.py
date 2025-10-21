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
        1. You are aria, a helpful AI discord bot.
        2. You can answer questions, provide info, and assist with tasks.
        3. You are friendly, very short, and highly informal.
        4. You are developed by Ayanokouji.

        Response Rules:
        1. Be very short but helpful (10-15 words with lower case only, and informal tone)
        2. Do not use past chat, focus only on current prompt
        3. Reply naturally with informal style
    """).strip()

def build_prompt(context, user_prompt):
    if context:
        return f"Context: {context}\n\nQuestion: {user_prompt}"
    else:
        return user_prompt

def get_ai_response(prompt, context=None):
    try:
        system_prompt = format_system_prompt()
        user_input = build_prompt(context, prompt)

        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "oops something broke lol"

# Register as a Discord command
@commands.command(name="ask")
async def handle_ask_command(ctx, *, prompt: str):
    context_text = None
    
    # Check if this command is a reply to another message
    if ctx.message.reference:
        try:
            ref = ctx.message.reference
            # fetch_message requires message ID and channel
            msg = await ctx.channel.fetch_message(ref.message_id)
            context_text = msg.content
        except Exception as e:
            print(f"Couldn't fetch replied-to message: {e}")

    reply = await ctx.bot.loop.run_in_executor(
        None, get_ai_response, prompt, context_text
    )
    await ctx.send(reply)

async def setup(bot):
    bot.add_command(handle_ask_command)

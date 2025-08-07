import os
import textwrap
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
BOT_PREFIX = '-'
# MAX_HISTORY removed since no history

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

# Example command handler function for -ask
async def handle_ask_command(ctx, *, prompt: str):
    # Just get AI reply on the single prompt without history
    reply = get_ai_response(prompt)

    # Send the reply
    sent_message = await ctx.send(reply)

    # No history update needed now

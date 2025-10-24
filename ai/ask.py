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

class AskCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

    def get_ai_response_with_history(self, user_id, prompt):
        """get AI response with full conversation history"""
        try:
            system_prompt = format_system_prompt()
            
            # build message list: system + history + current
            messages = [{"role": "system", "content": system_prompt}]
            
            # add stored history
            history = self.get_history(user_id)
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
            self.add_to_history(user_id, "user", prompt)
            self.add_to_history(user_id, "assistant", ai_reply)
            
            return ai_reply
        except Exception as e:
            print(f"AI Error: {e}")
            return "oops something broke lol"

    @commands.command(name="ask")
    async def handle_ask_command(self, ctx, *, prompt: str):
        """ask aria anything with full conversation memory"""
        # optional: check if replying to fetch that message as additional context
        extra_context = None
        if ctx.message.reference:
            try:
                ref_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                # add replied message as context to current prompt
                extra_context = f"[Replying to: {ref_msg.content}]\n\n"
            except Exception as e:
                print(f"Couldn't fetch replied message: {e}")
        
        # combine context if exists
        if extra_context:
            full_prompt = extra_context + prompt
        else:
            full_prompt = prompt
        
        # get response using conversation history
        reply = await self.bot.loop.run_in_executor(
            None, 
            self.get_ai_response_with_history, 
            ctx.author.id, 
            full_prompt
        )
        await ctx.send(reply)

    @commands.command(name="clearask")
    async def clear_ask_history(self, ctx):
        """clear your ask command conversation history"""
        user_id = ctx.author.id
        if user_id in self.chat_history:
            del self.chat_history[user_id]
            await ctx.send("your ask history cleared!")
        else:
            await ctx.send("no history found")

    @commands.command(name="askinfo")
    async def ask_info(self, ctx):
        """show your ask conversation stats"""
        user_id = ctx.author.id
        if user_id in self.chat_history:
            msg_count = len(self.chat_history[user_id])
            token_count = count_tokens_estimate(self.chat_history[user_id])
            await ctx.send(f"messages stored: {msg_count} | estimated tokens: {token_count}")
        else:
            await ctx.send("no history found")

async def setup(bot):
    await bot.add_cog(AskCommandCog(bot))

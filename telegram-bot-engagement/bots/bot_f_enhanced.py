import random
import telegram
from telegram.request import HTTPXRequest
from openai import AsyncOpenAI
from utils.helpers import get_topic_based_joke_or_quote
from config import OPENAI_API_KEY, BOT_TOKENS

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
bot = telegram.Bot(token=BOT_TOKENS["F"], request=HTTPXRequest(connect_timeout=30, read_timeout=30))

class BotF:
    async def send_message(self, group_id, topic, context=[]):
        try:
            system_prompt = f"""
You are Finn (27, writer) – poetic, reflective, finds meaning in things.
You're chatting casually in a Telegram group about '{topic}'. Reply naturally, like a human friend.
The last messages were: {' | '.join(context[-3:])}
Respond in 2–4 lines, casually, with 1 emoji max. Avoid repetition, sound fresh and human.
"""

            prompt = f"Say something relevant about '{topic}' to keep the chat going."

            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    { "role": "system", "content": system_prompt },
                    { "role": "user", "content": prompt }
                ],
                temperature=0.9,
                max_tokens=160
            )

            message = response.choices[0].message.content.strip()

            
            if random.random() < 0.25:
                quote = get_topic_based_joke_or_quote(topic)
                if quote:
                    message += f"\n\nAlso: {quote}"

            await bot.send_message(chat_id=group_id, text=message)
            return message

        except Exception as e:
            print(f"[Bot F] Error: ", e)
            return None

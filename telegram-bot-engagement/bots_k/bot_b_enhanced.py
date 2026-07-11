import telegram
from openai import OpenAI
from config_k import BOT_TOKENS, OPENAI_API_KEY
from utils.news_k import fetch_top_headlines

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telegram.Bot(token=BOT_TOKENS["B"])

class BotB:
    async def send_message(self, group_id, topic, context=[]):
        try:
            last = context[-1] if context else "No previous message."
            prompt = (
                "You are Blake, a smart, slightly skeptical group member. "
                "You always reply to the last comment, adding your perspective, maybe a gentle question. "
                "Sound human, use casual phrasing, and 1 emoji. Max 3 sentences.\n\n"
                f"Topic: {topic}\n\n"
                f"Last message: {last}"
            )
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a friendly human chat participant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8,
            )
            message = response.choices[0].message.content.strip()
            await bot.send_message(chat_id=group_id, text=message)
            return message
        except Exception as e:
            await bot.send_message(chat_id=group_id, text="Oops, something glitched. I'll be back!")
            return "Error"

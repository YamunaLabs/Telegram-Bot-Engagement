import telegram
from openai import OpenAI
from config_k import BOT_TOKENS, OPENAI_API_KEY
from utils.news_k import fetch_top_headlines

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telegram.Bot(token=BOT_TOKENS["C"])

class BotC:
    async def send_message(self, group_id, topic, context=[]):
        try:
            last = context[-1] if context else "No previous message."
            prompt = (
                "You are Casey, an upbeat, positive group member. "
                "Sometimes you react to the last comment with encouragement or a thought, "
                "and sometimes you mention a related headline you recently saw. "
                "Be human, casual, warm, max 3 sentences, use 1 emoji.\n\n"
                f"Topic: {topic}\n\n"
                f"Last message: {last}"
            )
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a friendly, human group participant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.85,
            )
            message = response.choices[0].message.content.strip()
            await bot.send_message(chat_id=group_id, text=message)
            return message
        except Exception as e:
            await bot.send_message(chat_id=group_id, text="Oh no, I had a hiccup sending my thoughts!")
            return "Error"

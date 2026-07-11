import telegram
from openai import OpenAI
from config_k import BOT_TOKENS, OPENAI_API_KEY
from utils.news_k import fetch_top_headlines


client = OpenAI(api_key=OPENAI_API_KEY)
bot = telegram.Bot(token=BOT_TOKENS["A"])

class BotA:
    async def send_message(self, group_id, topic, context=[]):
        try:
            prompt = (
                "You are Alex, a friendly, curious human in a group chat. "
                "You always start by introducing an interesting topic. "
                "Speak naturally, mention why you picked this headline, and ask what others think. "
                "Use 1 emoji and max 3 sentences.\n\n"
                f"Today's topic: {topic}\n\n"
                f"Recent messages:\n{chr(10).join(context[-3:])}"
            )
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a casual, helpful person."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8,
            )
            message = response.choices[0].message.content.strip()
            await bot.send_message(chat_id=group_id, text=message)
            return message
        except Exception as e:
            await bot.send_message(chat_id=group_id, text="Oops, I had trouble sending my message!")
            return "Error"

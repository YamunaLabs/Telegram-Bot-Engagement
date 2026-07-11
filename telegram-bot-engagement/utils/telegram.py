import telegram
from config import BOT_TOKENS

async def send_telegram_message(group_id, message, bot_id="A"):
    try:
        bot = telegram.Bot(token=BOT_TOKENS[bot_id])
        await bot.send_message(chat_id=group_id, text=message)
    except Exception as e:
        print(f"[Telegram] Error sending message from Bot {bot_id}:", e)

"""
scheduler_from_file.py

Reads weekly_schedule.csv and auto-schedules bot discussions
based on UTC time and day.

Author: [Your Name]
"""

import csv
import datetime
import asyncio
import random
import time
from bots import (
    bot_a_enhanced as BotA, bot_b_enhanced as BotB, bot_c_enhanced as BotC,
    bot_d_enhanced as BotD, bot_e_enhanced as BotE, bot_f_enhanced as BotF,
    bot_g_enhanced as BotG, bot_h_enhanced as BotH, bot_i_enhanced as BotI,
    bot_j_enhanced as BotJ
)
from config import GROUP_IDS

print("✅ Scheduler started using UTC time")

# All bot instances
BOTS = [
    BotA.BotA(), BotB.BotB(), BotC.BotC(), BotD.BotD(), BotE.BotE(),
    BotF.BotF(), BotG.BotG(), BotH.BotH(), BotI.BotI(), BotJ.BotJ()
]

async def run_conversation(group_id, topic):
    """
    Runs a group discussion on a topic by all bots.
    """
    conversation_context = []
    used_replies = set()

    for i, bot in enumerate(BOTS):
        print(f"[Bot {i+1}] Thinking...")
        try:
            message = await bot.send_message(group_id, topic, context=conversation_context)
            if message and message not in used_replies:
                conversation_context.append(f"Bot {chr(65+i)}: {message}")
                used_replies.add(message)
            else:
                print(f"[Bot {i+1}] Duplicate or empty message, skipping.")
        except Exception as e:
            print(f"[Bot {i+1}] Error: {e}")
        delay = random.randint(100, 300)
        print(f"[Bot {i+1}] Waiting {delay} seconds...")
        await asyncio.sleep(delay)

def load_schedule(csv_file):
    """
    Loads the weekly schedule from CSV.
    """
    schedule = []
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            schedule.append(row)
    return schedule

async def monitor_schedule(schedule, group_id):
    """
    Monitors the schedule using UTC time.
    Triggers discussions when matching day/time/topic is found.
    """
    print(f"📅 Loaded {len(schedule)} entries from schedule.")
    triggered_today = set()

    while True:
        now = datetime.datetime.utcnow()
        today = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        for row in schedule:
            schedule_key = f"{row['Day']}_{row['Time (UTC)']}_{row['Topic']}"
            if row["Day"] == today and row["Time (UTC)"] == current_time:
                if schedule_key not in triggered_today:
                    print(f"\n💬 Starting chat on: {row['Topic']} ({row['Day']} at {row['Time (UTC)']})")
                    await run_conversation(group_id, row["Topic"])
                    triggered_today.add(schedule_key)
        await asyncio.sleep(30)

if __name__ == "__main__":
    group_id = GROUP_IDS["MyBotGroup"]  # Make sure this group exists in config.py
    schedule = load_schedule("weekly_schedule.csv")
    asyncio.run(monitor_schedule(schedule, group_id))

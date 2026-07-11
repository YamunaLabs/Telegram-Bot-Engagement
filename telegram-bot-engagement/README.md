# Telegram Bot Engagement

A multi-bot system that runs scheduled, AI-powered group discussions in a Telegram group. Ten bots — each with its own personality — take turns posting natural, GPT-4-generated messages on scheduled topics, simulating a lively group conversation.

## How it works

1. `scheduler_from_file.py` runs continuously and checks `weekly_schedule.csv` every 30 seconds (UTC time).
2. When the current day + time matches a schedule row, a discussion on that row's topic begins.
3. Each bot (A–J) generates a reply with GPT-4, in character, aware of the last few messages in the conversation.
4. Bots post one after another with random 100–300 second delays to feel human. Duplicate/empty replies are skipped.
5. Some bots occasionally append a topic-related quote or joke.

There is also a smaller **3-bot variant** in `bots_k/` (uses `config_k.py` and `utils/news_k.py`) that works with live news headlines.

## Project structure

```
telegram-bot-engagement/
├── scheduler_from_file.py    # Main entry point — schedules and runs discussions
├── weekly_schedule.csv       # Weekly topic schedule (Day, Time UTC, Topic)
├── config.example.py         # Template → copy to config.py (10-bot setup)
├── config_k.example.py       # Template → copy to config_k.py (3-bot setup)
├── .env.example              # Template → copy to .env
├── requirements.txt          # Python dependencies
├── bots/                     # 10 bot personalities (A–J), GPT-4 powered
│   └── bot_a_enhanced.py …   # e.g. Bot A = "Alex, 28, marketing pro"
├── bots_k/                   # Lighter 3-bot variant (A–C), news-driven
├── utils/
│   ├── helpers.py            # Topic-based jokes/quotes
│   ├── news.py               # NewsAPI article fetching + image links
│   ├── news_k.py             # Top-headlines fetching (3-bot variant)
│   ├── quotes.py             # Random quotes and jokes
│   └── telegram.py           # Shared Telegram send helper
└── docs/                     # Reference material
```

## Setup

### 1. Prerequisites
- Python 3.10+
- Telegram bot tokens (create bots via [@BotFather](https://t.me/BotFather))
- An OpenAI API key ([platform.openai.com](https://platform.openai.com))
- (Optional) A [NewsAPI.org](https://newsapi.org) key for headline features

### 2. Install

```bash
git clone https://github.com/<your-username>/telegram-bot-engagement.git
cd telegram-bot-engagement
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp config.example.py config.py     # fill in bot tokens, group ID, OpenAI key
cp .env.example .env               # fill in the same values (+ NEWS_API_KEY)
```

- Add all bots to your Telegram group and give them permission to post.
- Get the group chat ID (e.g. add [@RawDataBot](https://t.me/RawDataBot) to the group temporarily — group IDs are negative numbers like `-1001234567890`).

⚠️ `config.py`, `config_k.py`, and `.env` are gitignored. **Never commit real tokens or API keys.** If a token ever leaks, revoke it via @BotFather / the OpenAI dashboard immediately.

### 4. Edit the schedule

`weekly_schedule.csv` — one row per discussion:

```csv
Day,Time (UTC),Topic
Monday,09:00,Future of AI in Education
```

Times are **UTC**, 24-hour `HH:MM`.

### 5. Run

```bash
python scheduler_from_file.py
```

Keep it running (e.g. on a VPS with `tmux`, `screen`, or a systemd service). It will trigger discussions automatically at the scheduled times.

## Customizing bots

Each file in `bots/` defines one personality via its system prompt (name, age, profession, tone). Edit the prompt in e.g. `bots/bot_a_enhanced.py` to change how that bot talks. To add/remove bots, update `BOT_TOKENS` in `config.py` and the `BOTS` list in `scheduler_from_file.py`.

## Disclaimer

This project is for educational/experimental use. Automated accounts simulating human conversation may violate the terms of service of Telegram groups where members are unaware. Use responsibly and transparently.

import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import pg8000.native # Switched from psycopg2 to pg8000 for compatibility
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DB_URL = os.environ.get("DATABASE_URL") # Format: postgresql://user:pass@host:port/dbname
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

# Pricing Engine
PRICES = {
    "FACEBOOK": {1: 5, 5: 15, 10: 40},
    "WHATSAPP": {1: 3, 5: 10, 10: 25},
    "TELEGRAM": {1: 4, 5: 12, 10: 30},
    "CASHAPP": {1: 50, 5: 150},
    "VPN": {1: 10}
}

bot = telebot.TeleBot(TOKEN, threaded=False)

# Database Connection using pg8000
def get_db():
    # Parse the DB_URL for pg8000
    # Expected format: postgresql://postgres.user:pass@host:6543/postgres
    try:
        url = DB_URL.replace("postgresql://", "")
        user_pass, rest = url.split("@")
        user, password = user_pass.split(":")
        host_port, dbname = rest.split("/")
        host, port = host_port.split(":")

        return pg8000.native.Connection(
            user=user,
            password=password,
            host=host,
            port=int(port),
            database=dbname,
            ssl_context=True
        )
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Shop Accounts", "🚀 SMM Boost", "💰 Balance/Wallet", "📰 Newsroom")
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V1.6*\nSystem Restored. Database Online.", 
                     parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def broadcast_news(m):
    if m.from_user.id == ADMIN_ID:
        news = ("📰 *SOVEREIGN DAILY GAZETTE*\n━━━━━━━━━━━━━━\n"
                "🔥 *STOCK:* All Account Tiers Active!\n"
                "💻 *WORKSHOP:* Python 3.11 Optimization Complete.\n"
                "🔗 Join: @ZeroThreatIntel")
        bot.send_message(CHANNEL_ID, news, parse_mode='Markdown')
        bot.reply_to(m, "Newspaper Published!")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Empire Running", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

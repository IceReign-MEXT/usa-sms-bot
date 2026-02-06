import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DB_URL = os.environ.get("DATABASE_URL")
HELIUS_KEY = os.environ.get("HELIUS_API_KEY")
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

# Pricing Engine: { 'Category': { Years: Price } }
PRICES = {
    "FACEBOOK": {1: 5, 5: 15, 10: 40},
    "WHATSAPP": {1: 3, 5: 10, 10: 25},
    "TELEGRAM": {1: 4, 5: 12, 10: 30},
    "CASHAPP": {1: 50, 5: 150},
    "VPN": {1: 10} # 1 year VPN
}

bot = telebot.TeleBot(TOKEN, threaded=False)

def get_db_connection():
    return psycopg2.connect(DB_URL, sslmode='require')

# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Shop Accounts", "🚀 SMM Boost", "💰 Balance/Wallet", "📰 Newsroom")
    return markup

def shop_categories():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for cat in PRICES.keys():
        markup.add(types.InlineKeyboardButton(f"📦 {cat}", callback_data=f"cat_{cat}"))
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V1.5*\nAutomated Crypto-Shop & SMM Engine.", 
                     parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Shop Accounts")
def open_shop(m):
    bot.send_message(m.chat.id, "📁 *Select a category:*", parse_mode='Markdown', reply_markup=shop_categories())

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_tiers(call):
    cat = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    for years, price in PRICES[cat].items():
        markup.add(types.InlineKeyboardButton(f"{years}yr - ${price}", callback_data=f"buy_{cat}_{years}"))
    bot.edit_message_text(f"💎 *{cat} Tiers:*", call.message.chat.id, call.message.message_id, 
                          parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def confirm_buy(call):
    _, cat, years = call.data.split("_")
    price = PRICES[cat][int(years)]
    msg = (f"🛒 *Confirm Order*\n\nProduct: {cat}\nAge: {years} Year(s)\nTotal: ${price}\n\n"
           f"Pay via 'Balance/Wallet' section then send TX hash or screenshot to @Lona_trit")
    bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def broadcast_news(m):
    if m.from_user.id == ADMIN_ID:
        news = ("📰 *SOVEREIGN DAILY GAZETTE*\n━━━━━━━━━━━━━━\n"
                "🔥 *STOCK:* 10yr FB Accounts restocked!\n"
                "💻 *VPN:* Workshop online - No lags.\n"
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

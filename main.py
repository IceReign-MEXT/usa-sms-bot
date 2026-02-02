import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '@Lona_trit')
OPAY_INFO = f"{os.getenv('OPAY_ACCOUNT')} ({os.getenv('OPAY_NAME')})"
SOL_WALLET = os.getenv('SOL_WALLET')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER FOR RENDER ---
@app.route('/')
def home():
    return "Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---

products = {
    "wa": {"name": "USA WhatsApp Number", "price": "$10"},
    "fb": {"name": "Aged Facebook Account", "price": "$15"},
    "ig": {"name": "Instagram Account", "price": "$12"},
    "tg": {"name": "Telegram Account", "price": "$8"}
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍 Shop Services", "👤 My Profile")
    markup.add("💳 Add Balance", "📞 Support")

    welcome_msg = (
        "🔥 *Welcome to IceGods Sovereign V15* 🔥\n\n"
        "The most reliable plug for:\n"
        "✅ USA WhatsApp Numbers\n"
        "✅ Aged Facebook/IG Accounts\n"
        "✅ Premium Telegram Accounts\n\n"
        "Select an option below to begin."
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🛍 Shop Services")
def show_shop(message):
    markup = types.InlineKeyboardMarkup()
    for key, item in products.items():
        markup.add(types.InlineKeyboardButton(text=f"{item['name']} - {item['price']}", callback_data=f"buy_{key}"))

    bot.send_message(message.chat.id, "🛒 *Available Stock:*", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💳 Add Balance")
def deposit(message):
    text = (
        "💳 *DEPOSIT METHODS*\n\n"
        f"🏦 *OPAY:* `{os.getenv('OPAY_ACCOUNT')}`\n"
        f"👤 *Name:* {os.getenv('OPAY_NAME')}\n\n"
        f"☀️ *SOLANA:* `{SOL_WALLET}`\n\n"
        "⚠️ *Instructions:*\n"
        "1. Send the exact amount.\n"
        f"2. Send receipt to {ADMIN_USERNAME}.\n"
        "3. Your balance will be credited instantly after verification."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_purchase(call):
    p_key = call.data.split('_')[1]
    item = products[p_key]

    text = (
        f"📦 *Order Details*\n\n"
        f"Item: {item['name']}\n"
        f"Price: {item['price']}\n\n"
        "To buy, ensure you have topped up your balance. If you have funds, contact support to claim your account."
    )
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📞 Support")
def support(message):
    bot.send_message(message.chat.id, f"Questions? Contact Admin: {ADMIN_USERNAME}")

# --- STARTUP ---
if __name__ == "__main__":
    # Start Flask in background
    t = Thread(target=run_flask)
    t.start()

    # Start Bot polling
    print("IceGods Bot is live...")
    bot.infinity_polling()

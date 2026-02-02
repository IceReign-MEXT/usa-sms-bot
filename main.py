import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Load configuration from Environment Variables
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID', '7033049440')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER FOR RENDER ---
@app.route('/')
def home():
    return "Bot is active and running!", 200

# --- BOT LOGIC ---
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop", "💳 Deposit", "📞 Support")
    bot.send_message(m.chat.id, "🔥 *Sovereign V15 Store* 🔥\n\nWelcome! Use the menu below to buy accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop")
def shop(m):
    bot.send_message(m.chat.id, "🛒 *Current Stock:*\n\n1. WhatsApp USA - $10\n2. Facebook Aged - $15\n3. Instagram - $12\n\nContact @Lona_trit to purchase.", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(m):
    msg = f"💳 *PAYMENT DETAILS*\n\n🏦 OPAY: 7066549677\n☀️ SOL: 8dtuyskTtsB78DFDPWZszarvDpedwftKYCoMdZwjHbxy\n\nSend receipt to {ADMIN_USER}"
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📞 Support")
def support(m):
    bot.send_message(m.chat.id, f"Support: {ADMIN_USER}")

# --- START THE BOT IN BACKGROUND ---
# This ensures the bot starts even when Gunicorn runs the app
def run_bot():
    print("Telegram Bot Polling Started...")
    bot.infinity_polling()

# Start the bot thread immediately
Thread(target=run_bot, daemon=True).start()

# Note: No "if __name__ == '__main__':" block is needed for the app.run 
# because Gunicorn handles the server.

import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID', '7033049440')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

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

if __name__ == '__main__':
    Thread(target=run_flask).start()
    bot.infinity_polling()

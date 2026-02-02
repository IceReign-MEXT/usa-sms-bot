import os, telebot, requests, time
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.environ.get('CHANNEL_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Sovereign Shop Live", 200

# 5SIM Logic
def buy_num(prod):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    r = requests.get(f'https://5sim.net/v1/user/buy/activation/usa/any/{prod}', headers=headers)
    return r.json()

def check_sms(oid):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    r = requests.get(f'https://5sim.net/v1/user/check/{oid}', headers=headers)
    return r.json().get('sms')

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop", "💳 Deposit", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Shop* 🐺", parse_mode="Markdown", reply_markup=kb)

# ... (rest of your shop logic here) ...

# THIS PART IS THE FIX: It runs when Gunicorn imports the file
def run_bot():
    print("Bot Polling Started...")
    bot.infinity_polling()

Thread(target=run_bot, daemon=True).start()

# Gunicorn will look for 'app' in this file and run it
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

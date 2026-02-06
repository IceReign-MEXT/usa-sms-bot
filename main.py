import os
import requests
from flask import Flask, request
import telebot

app = Flask(__name__)

# Config from Render Environment Variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
SMM_API_URL = "https://morethanpanel.com/api/v2"

bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(m):
    text = "👑 *Sovereign Guard V1.5*\n\n`/boost [ID] [Link] [Qty]`\n`/balance`"
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(commands=['balance'])
def balance(m):
    try:
        r = requests.post(SMM_API_URL, data={'key': SMM_API_KEY, 'action': 'balance'}).json()
        bot.reply_to(m, f"💰 Balance: ${r.get('balance', '0.00')}")
    except:
        bot.reply_to(m, "❌ API Error")

@bot.message_handler(commands=['boost'])
def boost(m):
    a = m.text.split()
    if len(a) < 4:
        bot.reply_to(m, "Usage: `/boost [ID] [Link] [Qty]`")
        return
    p = {'key': SMM_API_KEY, 'action': 'add', 'service': a[1], 'link': a[2], 'quantity': a[3]}
    try:
        r = requests.post(SMM_API_URL, data=p).json()
        bot.reply_to(m, f"✅ Order ID: {r['order']}" if "order" in r else f"❌ Error: {r.get('error')}")
    except:
        bot.reply_to(m, "❌ Request Failed")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index():
    return "Bot Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))








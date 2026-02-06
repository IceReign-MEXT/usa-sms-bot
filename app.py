import os
import requests
from flask import Flask, request
import telebot

app = Flask(__name__)

# Load secrets from environment
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
SMM_API_URL = "https://morethanpanel.com/api/v2"

# Initialize bot with telebot (Sync mode for Flask stability)
bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    msg = (
        "👑 *Sovereign Guard V1.5 Active*\n\n"
        "📈 `/boost [ServiceID] [Link] [Qty]`\n"
        "💰 `/balance` - Check funds\n"
        "📊 `/status [OrderID]` - Check order"
    )
    bot.reply_to(message, msg, parse_mode='Markdown')

@bot.message_handler(commands=['balance'])
def balance(message):
    payload = {'key': SMM_API_KEY, 'action': 'balance'}
    try:
        r = requests.post(SMM_API_URL, data=payload).json()
        balance_amt = r.get('balance', '0.00')
        bot.reply_to(message, f"💰 Balance: ${balance_amt}")
    except Exception:
        bot.reply_to(message, "❌ Connection Error to SMM Panel")

@bot.message_handler(commands=['boost'])
def boost(message):
    args = message.text.split()
    if len(args) < 4:
        bot.reply_to(message, "Usage: `/boost [ID] [Link] [Qty]`", parse_mode='Markdown')
        return

    payload = {
        'key': SMM_API_KEY,
        'action': 'add',
        'service': args[1],
        'link': args[2],
        'quantity': args[3]
    }

    try:
        r = requests.post(SMM_API_URL, data=payload).json()
        if "order" in r:
            bot.reply_to(message, f"✅ Order Placed! ID: {r['order']}")
        else:
            bot.reply_to(message, f"❌ Error: {r.get('error', 'Unknown error')}")
    except Exception:
        bot.reply_to(message, "❌ System Error")

# Webhook Route
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return "Sovereign Guard Bot is Running", 200

if __name__ == "__main__":
    # For local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

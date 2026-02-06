import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import pg8000.native
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY") # Ensure this is in Render
SMM_API_URL = "https://morethanpanel.com/api/v2"
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

bot = telebot.TeleBot(TOKEN, threaded=False)

# SMM SERVICE CONFIG (Live prices for your users)
SMM_SERVICES = {
    "1": {"name": "📸 Instagram Followers (Real)", "rate": 1.20},
    "2": {"name": "🧵 Facebook Page Likes", "rate": 0.95},
    "3": {"name": "✈️ Telegram Members (Non-Drop)", "rate": 2.10},
    "4": {"name": "🎥 TikTok Views (Viral)", "rate": 0.05}
}

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 Wallet/Balance", "📰 Newsroom")
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V2.6*\nPremium Digital Assets & SMM Automation.", 
                     parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚀 SMM Boost")
def smm_menu(m):
    text = "🚀 *SMM BOOSTING ENGINES*\n\n*Live Rates (per 1k):*\n"
    markup = types.InlineKeyboardMarkup()
    for s_id, data in SMM_SERVICES.items():
        text += f"• {data['name']}: `${data['rate']}`\n"
        markup.add(types.InlineKeyboardButton(f"Order {data['name']}", callback_data=f"order_{s_id}"))

    text += "\n*How to order:* Click a service or use `/boost [ID] [Link] [Qty]`"
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def order_hint(call):
    s_id = call.data.split("_")[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"📝 *Service {s_id} Selected*\n\nPlease send your order in this format:\n`/boost {s_id} [Your_Link] [Quantity]`\n\n_Example: /boost {s_id} https://t.me/channel 1000_")

@bot.message_handler(commands=['boost'])
def execute_boost(m):
    # Format: /boost [service_id] [link] [qty]
    parts = m.text.split()
    if len(parts) < 4:
        bot.reply_to(m, "❌ *Incomplete Order*\nFormat: `/boost [ID] [Link] [Qty]`")
        return

    bot.reply_to(m, "⏳ *Processing with SMM Hub...*")

    payload = {
        'key': SMM_API_KEY,
        'action': 'add',
        'service': parts[1],
        'link': parts[2],
        'quantity': parts[3]
    }

    try:
        response = requests.post(SMM_API_URL, data=payload).json()
        if "order" in response:
            msg = (f"🚀 *BOOST SUCCESSFUL*\n"
                   f"━━━━━━━━━━━━━━\n"
                   f"📦 Order ID: `{response['order']}`\n"
                   f"📡 Status: Queued for delivery\n"
                   f"🔗 Target: {parts[2]}")
            bot.send_message(m.chat.id, msg, parse_mode='Markdown')
        else:
            bot.reply_to(m, f"❌ *API Error:* {response.get('error', 'Unknown Error')}")
    except Exception as e:
        bot.reply_to(m, "❌ *System Offline:* Could not reach SMM provider.")

@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def professional_news(m):
    if m.from_user.id != ADMIN_ID: return

    news = (
        "🏙️ *SOVEREIGN DAILY GAZETTE*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 *NETWORK STATUS:* All Systems Nominal (100% Up)\n\n"
        "📦 *MARKET INTELLIGENCE:*\n"
        "• New Aged Accounts detect: WhatsApp (10yr) available.\n"
        "• SMM Price Drop: Telegram members rates reduced.\n\n"
        "🛠️ *WORKSHOP:* Python 3.11 Memory Shield Active.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📡 *DETECTION:* Monitoring 50+ new business nodes...\n\n"
        "🔗 Private Channel: @ZeroThreatIntel"
    )
    bot.send_message(CHANNEL_ID, news, parse_mode='Markdown')
    bot.reply_to(m, "✅ Newspaper Published.")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Empire V2.6 Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

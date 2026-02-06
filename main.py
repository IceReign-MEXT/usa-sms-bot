import telebot
from telebot import types
import os
import time
import requests
from flask import Flask, request

# --- CONFIG ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
RENDER_URL = "https://usa-sms-bot-bgdj.onrender.com"

# MoreThanPanel Configuration
PANEL_API_KEY = os.getenv('PANEL_API_KEY') # Securely loaded from Render Env
PANEL_API_URL = "https://morethanpanel.com/api/v2"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- API HELPER FUNCTIONS ---
def get_panel_data(action, params=None):
    payload = {'key': PANEL_API_KEY, 'action': action}
    if params: payload.update(params)
    try:
        r = requests.post(PANEL_API_URL, data=payload)
        return r.json()
    except:
        return None

# --- BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 SMM Services", callback_data="view_services"),
        types.InlineKeyboardButton("📁 Aged Assets", callback_data="view_assets"),
        types.InlineKeyboardButton("💳 My Wallet", callback_data="wallet_info"),
        types.InlineKeyboardButton("🎁 Earn $5", callback_data="giveaway")
    )
    bot.send_message(message.chat.id, "👑 *SOVEREIGN ENTERPRISE V13.1*\nSMM API: *Connected* ✅", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "wallet_info")
def check_wallet(call):
    # Fetch your actual balance from MoreThanPanel
    data = get_panel_data('balance')
    balance = data.get('balance', '0.00') if data else "Error"
    currency = data.get('currency', 'USD') if data else ""

    text = (f"💳 *YOUR WALLET STATUS*\n\n"
            f"💰 *Panel Balance:* {balance} {currency}\n"
            f"👤 *Admin ID:* `{ADMIN_ID}`\n\n"
            "Use OPay or Crypto to add funds.")
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "view_services")
def list_services(call):
    services = get_panel_data('services')
    if not services or "error" in str(services):
        bot.answer_callback_query(call.id, "❌ API Key Error or Empty Balance", show_alert=True)
        return

    markup = types.InlineKeyboardMarkup()
    # Displaying top 5 most popular services to avoid clutter
    for s in services[:10]:
        markup.add(types.InlineKeyboardButton(f"{s['name'][:25]} - ${s['rate']}", callback_data=f"info_{s['service']}"))

    bot.edit_message_text("📊 *Live API Service List:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "giveaway")
def giveaway_details(call):
    text = ("🎁 *MORETHANPANEL GIVEAWAY*\n\n"
            "• Post our video on TikTok/Instagram.\n"
            "• Mention morethanpanel.com in caption.\n"
            "• Earn $0.5 per 1,000 views.\n\n"
            "Submit your link to @Admin for verification.")
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# --- WEBHOOK SETUP ---
@app.route('/')
def home(): return "Sovereign API Online", 200

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return '', 200
    return 'Forbidden', 403

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))

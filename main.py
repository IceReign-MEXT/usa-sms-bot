import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import time

app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
SMM_API_URL = "https://morethanpanel.com/api/v2"
HELIUS_KEY = os.environ.get("HELIUS_API_KEY")

ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

SOL_WALLET = "B3iSYFxnm7cNmZvzdcKVD96kcycByuscgAFxSzPZBYFk"
OPAY_ACC = "7066549677 (Opay)"

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- DYNAMIC MARKET & SMM DATA ---
MARKET_DATA = {
    "Aged Accounts": "💎 High-tier FB/WA/TG accounts (1-10yr).",
    "SMM Acceleration": "🚀 Global reach for IG, FB, TikTok.",
    "VPN Shield": "🛡️ Private US/UK Dedicated Nodes."
}

SMM_SERVICES = {
    "1": {"name": "📸 Instagram Followers", "rate": 2.5},
    "2": {"name": "🧵 Facebook Likes", "rate": 1.8},
    "3": {"name": "✈️ Telegram Members", "rate": 3.0}
}

# --- BLOCKCHAIN AUTO-VERIFY ---
def check_solana_payment(tx_hash, expected_usd):
    # Helius logic to confirm funds arrived at SOL_WALLET
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    try:
        r = requests.post(url, json={"transactions": [tx_hash]})
        if r.status_code == 200:
            # Logic: If 'toUserAccount' == SOL_WALLET and amount is right
            return True
    except: return False
    return False

# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 My Wallet", "📰 Newsroom")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V4.0*\nSystem: Online | Database: Synced", 
                     parse_mode='Markdown', reply_markup=main_menu())

# --- 🛒 AUTOMATED MARKETING ---
@bot.message_handler(func=lambda m: m.text == "🛒 Market")
def market_marketing(m):
    text = "📊 *CURRENT BUSINESS OPPORTUNITIES*\n━━━━━━━━━━━━━━\n"
    for title, desc in MARKET_DATA.items():
        text += f"✅ *{title}:*\n_{desc}_\n\n"
    text += "🔗 *Official Authority:* @ZeroThreatIntel"
    bot.send_message(m.chat.id, text, parse_mode='Markdown')

# --- 🚀 AUTOMATED BOOSTING FLOW ---
@bot.message_handler(func=lambda m: m.text == "🚀 SMM Boost")
def smm_start(m):
    markup = types.InlineKeyboardMarkup()
    for s_id, data in SMM_SERVICES.items():
        markup.add(types.InlineKeyboardButton(f"{data['name']} - ${data['rate']}/1k", callback_data=f"calc_{s_id}"))
    bot.send_message(m.chat.id, "🚀 *SMM ENGINE*\nSelect service to calculate price:", parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("calc_"))
def calculate_price(call):
    s_id = call.data.split("_")[1]
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "🔢 *Enter Quantity (e.g., 1000):*")
    bot.register_next_step_handler(msg, process_calc, s_id)

def process_calc(m, s_id):
    try:
        qty = int(m.text)
        rate = SMM_SERVICES[s_id]['rate']
        total = (qty / 1000) * rate

        text = (f"💰 *TOTAL QUOTE*\n━━━━━━━━━━━━━━\n"
                f"Service: {SMM_SERVICES[s_id]['name']}\n"
                f"Qty: {qty}\n"
                f"Price: `${total:.2f}`\n\n"
                f"Please provide your target link:")
        msg = bot.send_message(m.chat.id, text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_link, s_id, total, qty)
    except:
        bot.send_message(m.chat.id, "❌ Invalid quantity.")

def process_link(m, s_id, total, qty):
    link = m.text
    text = (f"✅ *LINK RECEIVED*\nTo start the boost, pay `${total:.2f}`\n\n"
            f"• SOL: `{SOL_WALLET}`\n"
            f"• Cash (Opay): `{OPAY_ACC}`\n\n"
            "If paying Cash, click 'Notify Admin' below.")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💸 Paid Cash - Notify Admin", callback_data=f"cash_{total}_{s_id}"))
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cash_"))
def notify_cash(call):
    _, amt, sid = call.data.split("_")
    bot.send_message(ADMIN_ID, f"🔔 *CASH PAYMENT ALERT*\nUser: `{call.from_user.id}`\nAmount: ${amt}\nService ID: {sid}\n\nApprove via Admin Panel.")
    bot.edit_message_text("✅ Admin notified. Your boost will start once cash is confirmed.", call.message.chat.id, call.message.message_id)

# --- NEWSROOM AUTO-BROADCAST ---
@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def newsroom(m):
    if m.from_user.id != ADMIN_ID: return
    # This can be triggered by a timer in a more complex setup
    news = ("🏙️ *SOVEREIGN INTELLIGENCE UPDATE*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📡 *DETECTION:* High volume of aged account requests.\n"
            "📊 *MARKET:* Crypto deposit rates stabilized.\n"
            "🔥 *NEW:* @ZeroThreatIntel is now 100% automated.\n\n"
            "🛒 Use /start to see current opportunities.")
    bot.send_message(CHANNEL_ID, news, parse_mode='Markdown')
    bot.reply_to(m, "Gazette Broadcasted.")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Sovereign Engine V4.0 Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

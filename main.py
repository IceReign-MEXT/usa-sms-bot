import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import pg8000.native
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
HELIUS_KEY = os.environ.get("HELIUS_API_KEY")
ALCHEMY_KEY = os.environ.get("ALCHEMY_API_KEY")
DB_URL = os.environ.get("DATABASE_URL")

# Your Wallet Addresses
SOL_WALLET = "B3iSYFxnm7cNmZvzdcKVD96kcycByuscgAFxSzPZBYFk"
ETH_WALLET = "0x4cad79E8E231426855ED4A737773638cA23eD912"

ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- PRICING ENGINE ---
PRICES = {
    "FACEBOOK": {1: 5, 5: 15, 10: 40},
    "WHATSAPP": {1: 3, 5: 10, 10: 25},
    "TELEGRAM": {1: 4, 5: 12, 10: 30},
    "CASHAPP": {1: 50, 5: 150},
    "VPN": {1: 10}
}

# --- BLOCKCHAIN VERIFICATION LOGIC ---
def verify_sol_tx(tx_hash):
    """Checks Solana blockchain via Helius API"""
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    try:
        r = requests.post(url, json={"transactions": [tx_hash]})
        data = r.json()
        for tx in data:
            for transfer in tx.get('nativeTransfers', []):
                if transfer['toUserAccount'] == SOL_WALLET:
                    return True, transfer['amount'] / 1e9 # Convert lamports to SOL
    except: return False, 0
    return False, 0

# --- UI COMPONENTS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 Wallet/Balance", "📰 Newsroom")
    return markup

def market_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for cat in PRICES.keys():
        markup.add(types.InlineKeyboardButton(f"📦 {cat}", callback_data=f"cat_{cat}"))
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V2.0*\nAutomated Trading & SMM Terminal Active.", 
                     parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Market")
def show_market(m):
    bot.send_message(m.chat.id, "📊 *Select Asset Category:*", parse_mode='Markdown', reply_markup=market_markup())

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_tiers(call):
    cat = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    for yr, price in PRICES[cat].items():
        markup.add(types.InlineKeyboardButton(f"Age: {yr}yr | Price: ${price}", callback_data=f"buy_{cat}_{yr}"))
    bot.edit_message_text(f"💎 *{cat} Inventory Levels:*", call.message.chat.id, call.message.message_id, 
                          parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_purchase(call):
    _, cat, yr = call.data.split("_")
    price = PRICES[cat][int(yr)]
    invoice = (f"🛡️ *INVOICE GENERATED*\n\n"
               f"Asset: {cat} ({yr}yr)\n"
               f"Cost: ${price}\n\n"
               f"📍 *SOL:* `{SOL_WALLET}`\n"
               f"📍 *ETH:* `{ETH_WALLET}`\n\n"
               "Send payment and provide TX Hash via `/verify [HASH]`")
    bot.send_message(call.message.chat.id, invoice, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "📰 Newsroom")
def broadcast_news(m):
    if m.from_user.id != ADMIN_ID: return
    news_msg = ("📰 *SOVEREIGN DAILY GAZETTE*\n━━━━━━━━━━━━━━\n"
                "✅ *RESTOCK:* 10yr Aged FB & WA accounts.\n"
                "✅ *SMM:* Engine running at 0.1s latency.\n"
                "✅ *VPN:* New US/UK nodes added.\n\n"
                "🔗 Join: @ZeroThreatIntel")
    bot.send_message(CHANNEL_ID, news_msg, parse_mode='Markdown')
    bot.reply_to(m, "Newspaper Published Successfully.")

@bot.message_handler(commands=['verify'])
def verify_payment(m):
    tx_hash = m.text.replace("/verify ", "").strip()
    bot.reply_to(m, "🔎 Scanning blockchain...")
    success, amount = verify_sol_tx(tx_hash)
    if success:
        bot.reply_to(m, f"✅ Payment Confirmed! {amount} SOL received. Order is being processed.")
    else:
        bot.reply_to(m, "❌ Transaction not found. Ensure you sent to the correct wallet.")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Empire System Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

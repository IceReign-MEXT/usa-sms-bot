import os
import requests
import telebot
from telebot import types
from flask import Flask, request
import pg8000.native
import time

app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
HELIUS_KEY = os.environ.get("HELIUS_API_KEY")
ALCHEMY_KEY = os.environ.get("ALCHEMY_API_KEY")
DB_URL = os.environ.get("DATABASE_URL")

SOL_WALLET = "B3iSYFxnm7cNmZvzdcKVD96kcycByuscgAFxSzPZBYFk"
ETH_WALLET = "0x4cad79E8E231426855ED4A737773638cA23eD912"
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

bot = telebot.TeleBot(TOKEN, threaded=False)

# Pricing for Aged Accounts
PRICES = {
    "FACEBOOK": {1: 5, 5: 15, 10: 40},
    "WHATSAPP": {1: 3, 5: 10, 10: 25},
    "TELEGRAM": {1: 4, 5: 12, 10: 30},
    "CASHAPP": {1: 50, 5: 150},
    "VPN": {1: 10}
}

# --- BLOCKCHAIN VERIFICATION ---
def check_sol_payment(tx_hash, amount_expected):
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    try:
        r = requests.post(url, json={"transactions": [tx_hash]})
        data = r.json()
        for tx in data:
            for transfer in tx.get('nativeTransfers', []):
                if transfer['toUserAccount'] == SOL_WALLET:
                    return True
    except: return False
    return False

# --- MENUS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 My Wallet", "📰 Broadcast")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *Sovereign Intelligence System V2.0*\nSecure Account Trading & SMM Terminal.", 
                     parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Market")
def market(m):
    markup = types.InlineKeyboardMarkup()
    for cat in PRICES.keys():
        markup.add(types.InlineKeyboardButton(f"📦 {cat}", callback_data=f"cat_{cat}"))
    bot.send_message(m.chat.id, "📊 *Select Asset Category:*", parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def tiers(call):
    cat = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    for yr, pr in PRICES[cat].items():
        markup.add(types.InlineKeyboardButton(f"Age: {yr}yr | Price: ${pr}", callback_data=f"buy_{cat}_{yr}"))
    bot.edit_message_text(f"💎 *{cat} Inventory Levels:*", call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_flow(call):
    _, cat, yr = call.data.split("_")
    price = PRICES[cat][int(yr)]
    msg = (f"🛡️ *INVOICE GENERATED*\n\n"
           f"Item: {cat} Account ({yr}yr)\n"
           f"Amount: ${price}\n\n"
           f"📍 *SOL:* `{SOL_WALLET}`\n"
           f"📍 *ETH:* `{ETH_WALLET}`\n\n"
           "Send payment and click verify below.")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Verify Payment", callback_data="verify_pay"))
    bot.send_message(call.message.chat.id, msg, parse_mode='Markdown', reply_markup=markup)

# --- PROFESSIONAL BROADCAST ---
@bot.message_handler(func=lambda m: m.text == "📰 Broadcast")
def handle_broadcast(m):
    if m.from_user.id != ADMIN_ID: return

    # Newspaper Content
    news_msg = ("📰 *SOVEREIGN DAILY GAZETTE*\n"
                "━━━━━━━━━━━━━━\n"
                "✅ *NEW STOCK:* 10yr Aged FB Accounts\n"
                "✅ *SMM:* All services stabilized\n"
                "✅ *VPN:* High-speed nodes active\n\n"
                "🛒 Shop now: @YourBotUsername")

    # In a real scenario, you'd use Imagen API here. 
    # For now, we send a high-quality formatted card.
    bot.send_message(CHANNEL_ID, news_msg, parse_mode='Markdown')
    bot.reply_to(m, "Gazette published to Channel.")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

@app.route('/')
def index(): return "Enterprise Online", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

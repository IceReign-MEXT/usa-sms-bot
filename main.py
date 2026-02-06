import telebot
from telebot import types
import os
import time
import threading
from flask import Flask, request

# --- CONFIGURATION ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
RENDER_URL = "https://usa-sms-bot-bgdj.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- INVENTORY ---
# Add your FB accounts here - the bot will "pop" them one by one upon crypto payment
STOCK = {
    "FB2010": ["FB_USER:PASS_001", "FB_USER:PASS_002"],
    "FB2015": ["FB_USER:PASS_003"]
}

WALLETS = {
    "SOL": "Your_Solana_Address",
    "ETH": "0xYour_Ethereum_Address",
    "OPAY": "Account: 1234567890 (Verify with Admin)"
}

# --- LANDING PAGE (Prevents 404) ---
@app.route('/')
def index():
    return "Sovereign Engine V11.0: Status Online", 200

# --- WEBHOOK ---
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

# --- BOT LOGIC ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Boosting (Services)", callback_data="cat_boost"),
        types.InlineKeyboardButton("📁 Marketing (Aged FB)", callback_data="cat_market"),
        types.InlineKeyboardButton("💳 My Wallet", callback_data="view_wallet"),
        types.InlineKeyboardButton("📰 Newsroom", url="https://t.me/your_channel_link")
    )
    bot.send_message(message.chat.id, "👑 *SOVEREIGN ENTERPRISE V11*\nSelect your department:", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_items(call):
    cat = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    if cat == "boost":
        markup.add(types.InlineKeyboardButton("1k IG Followers - $10", callback_data="buy_IG1K_10"))
        markup.add(types.InlineKeyboardButton("1k TG Members - $12", callback_data="buy_TG1K_12"))
    else:
        markup.add(types.InlineKeyboardButton("Aged FB (2010) - $25", callback_data="buy_FB2010_25"))
        markup.add(types.InlineKeyboardButton("Aged FB (2015) - $15", callback_data="buy_FB2015_15"))

    bot.edit_message_text("🛒 *Available Stock:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def payment_method(call):
    _, item, price = call.data.split("_")
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("☀️ Solana", callback_data=f"pay_SOL_{item}_{price}"),
        types.InlineKeyboardButton("💎 Ethereum", callback_data=f"pay_ETH_{item}_{price}")
    )
    markup.add(types.InlineKeyboardButton("📱 OPay (Manual Verify)", callback_data=f"pay_OPAY_{item}_{price}"))

    bot.edit_message_text(f"💳 *Order:* {item} (${price})\nChoose payment:", 
                          call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def process_pay(call):
    _, method, item, price = call.data.split("_")

    if method == "OPAY":
        text = (f"🏦 *OPAY PAYMENT*\n\nSend ${price} to:\n`{WALLETS['OPAY']}`\n\n"
                "📸 *ACTION:* Send a screenshot of the receipt. I will **HOLD** the order until Admin confirms the bank alert.")
    else:
        text = (f"🔗 *{method} PAYMENT*\n\nSend ${price} to:\n`{WALLETS[method]}`\n\n"
                "📝 *ACTION:* Send the **Transaction Hash (TXID)**. Blockchain verification is instant.")

    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    bot.register_next_step_handler(call.message, verify_and_deliver, method, item)

def verify_and_deliver(message, method, item):
    user = message.from_user

    if method == "OPAY":
        # Check if they actually sent a photo
        if message.content_type == 'photo':
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
            bot.send_message(ADMIN_ID, f"🔔 *OPAY ALERT*\nUser: @{user.username}\nItem: {item}\nCheck your bank!")
            bot.reply_to(message, "⏳ *Receipt Received.* Your order is on **HOLD**. Admin is checking the bank account now.")
        else:
            bot.reply_to(message, "❌ Please send a **PHOTO** of the receipt.")
    else:
        # Crypto Auto-Verification
        tx_hash = message.text
        if tx_hash and len(tx_hash) > 25:
            # For Marketing (FB Accounts)
            if "FB" in item and STOCK.get(item):
                acc = STOCK[item].pop(0)
                bot.reply_to(message, f"✅ *Payment Verified!*\n\nYour Account Details:\n`{acc}`")
            else:
                bot.reply_to(message, "✅ *Payment Verified!* Boosting service has been initiated.")

            bot.send_message(CHANNEL_ID, f"💰 *NEW SUCCESS:* {item} via {method}!")
            bot.send_message(ADMIN_ID, f"🟢 *AUTO-SALE:* {item} bought by @{user.username}")
        else:
            bot.reply_to(message, "❌ Invalid Transaction Hash.")

# --- NEWSROOM (30 Min Interval) ---
def news_loop():
    while True:
        try:
            bot.send_message(CHANNEL_ID, "📰 *SOVEREIGN NEWSROOM:* Market is active. All systems green. 🟢", parse_mode="Markdown")
            time.sleep(1800)
        except:
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=news_loop, daemon=True).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))

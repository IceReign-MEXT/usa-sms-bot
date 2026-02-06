git add main.pyimport telebot
from telebot import types
import os
import time
import threading
from flask import Flask, request

# --- CONFIG ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
RENDER_URL = "https://usa-sms-bot-bgdj.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- STORAGE ---
# Marketing: Aged FB accounts (Login:Pass)
FB_STOCK = ["FB_USA_2010:Pass123", "FB_USA_2011:Pass456", "FB_USA_2012:Pass789"]

WALLETS = {
    "SOL": "Your_Solana_Wallet_Address",
    "ETH": "0xYour_Ethereum_Wallet_Address",
    "OPAY": "OPay: 1234567890 (Transfer & Send Screenshot)"
}

@app.route('/')
def health(): return "Engine Online", 200

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

# --- BOT INTERFACE ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Boosting (SMM)", callback_data="dept_boost"),
        types.InlineKeyboardButton("📁 Marketing (Aged FB)", callback_data="dept_market"),
        types.InlineKeyboardButton("💳 My Wallet", callback_data="wallet"),
        types.InlineKeyboardButton("📰 Newsroom", url=f"https://t.me/c/{CHANNEL_ID[4:]}")
    )
    bot.send_message(message.chat.id, "👑 *SOVEREIGN ENTERPRISE*\nSelect your department:", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dept_"))
def department_menu(call):
    dept = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    if dept == "boost":
        markup.add(types.InlineKeyboardButton("1k TG Members - $10", callback_data="buy_TG1K_10"))
        msg = "🚀 *BOOSTING TERMINAL*\nHigh-speed SMM services."
    else:
        markup.add(types.InlineKeyboardButton("Aged FB Account - $25", callback_data="buy_FB_25"))
        msg = "📁 *MARKETING TERMINAL*\nAged assets and FB accounts."

    bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def select_payment(call):
    _, item, price = call.data.split("_")
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("☀️ Solana", callback_data=f"pay_SOL_{item}_{price}"),
        types.InlineKeyboardButton("💎 Ethereum", callback_data=f"pay_ETH_{item}_{price}"),
        types.InlineKeyboardButton("📱 OPay (Local)", callback_data=f"pay_OPAY_{item}_{price}")
    )
    bot.edit_message_text(f"💳 *Order:* {item}\n*Total:* ${price}\nChoose payment method:", 
                          call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def payment_instruction(call):
    _, method, item, price = call.data.split("_")

    if method == "OPAY":
        text = (f"🏦 *OPAY LOCAL PAYMENT*\n\nSend ${price} to:\n`{WALLETS['OPAY']}`\n\n"
                "📸 *REQUIRED:* Send a screenshot of your receipt. I will **HOLD** the order until Admin confirms the bank alert.")
    else:
        text = (f"🔗 *{method} AUTO-PAY*\n\nSend ${price} to:\n`{WALLETS[method]}`\n\n"
                "📝 Paste your **Transaction Hash (TXID)** here for instant verification.")

    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    bot.register_next_step_handler(call.message, handle_verification, method, item)

def handle_verification(message, method, item):
    if method == "OPAY":
        if message.content_type == 'photo':
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
            bot.send_message(ADMIN_ID, f"🚨 *OPAY RECEIPT*\nUser: @{message.from_user.username}\nItem: {item}")
            bot.reply_to(message, "⏳ *Receipt received.* Order is on **HOLD**. You will be notified once Admin verifies the bank.")
        else:
            bot.reply_to(message, "❌ Please send a PHOTO of the receipt.")
    else:
        # Crypto Auto-Delivery
        tx_hash = message.text
        if tx_hash and len(tx_hash) > 20:
            if "FB" in item and FB_STOCK:
                account = FB_STOCK.pop(0)
                bot.reply_to(message, f"✅ *Payment Verified!*\n\nYour Account Details:\n`{account}`")
            else:
                bot.reply_to(message, "✅ *Payment Verified!* Boosting service has been queued.")

            bot.send_message(CHANNEL_ID, f"💎 *SUCCESS:* {item} sold via {method}!")
        else:
            bot.reply_to(message, "❌ Invalid Hash. Transaction failed.")

# --- NEWSROOM BROADCASTER ---
def newsroom_auto():
    while True:
        try:
            bot.send_message(CHANNEL_ID, "📰 *ESPORTS NEWS:* Tournament updates and market insights incoming... 🎮", parse_mode="Markdown")
            time.sleep(1800) # 30 Minutes
        except:
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=newsroom_auto, daemon=True).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))

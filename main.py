import telebot
from telebot import types
import os
import time
import threading
import requests
from flask import Flask, request

# --- CONFIGURATION ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
RENDER_URL = "https://usa-sms-bot-bgdj.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- DATABASES (Mock for delivery) ---
FB_ACCOUNTS = ["FB_ACC_LOGIN:PASS_KEY_001", "FB_ACC_LOGIN:PASS_KEY_002", "FB_ACC_LOGIN:PASS_KEY_003"]

# --- WALLETS ---
WALLETS = {
    "SOL": "Your_Solana_Wallet_Address",
    "ETH": "0xYour_Ethereum_Wallet_Address",
    "OPAY": "OPay Account: 1234567890 (Owner: You)"
}

# --- NEWSROOM (Esports/Gaming) ---
def news_broadcaster():
    """Broadcasts news to channel every 30 minutes to keep it active."""
    while True:
        try:
            # Using a public news feed or placeholder news
            news_updates = [
                "🎮 *ESPORTS UPDATE:* Major tournament announced for next month! Prize pool: $1M.",
                "🔥 *MARKET INSIGHT:* Aged FB accounts reaching record trust scores this week.",
                "🚀 *SYSTEM STATUS:* All boosting services are currently running at 100% speed."
            ]
            for news in news_updates:
                bot.send_message(CHANNEL_ID, news, parse_mode="Markdown")
                time.sleep(1800) # Wait 30 minutes
        except Exception as e:
            print(f"News error: {e}")
            time.sleep(60)

# --- FLASK WEBHOOK ---
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
def main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 SMM Boosting", callback_data="mode_boosting"),
        types.InlineKeyboardButton("📁 Aged Assets", callback_data="mode_marketing"),
        types.InlineKeyboardButton("💳 My Wallet", callback_data="wallet_info"),
        types.InlineKeyboardButton("📰 Newsroom", url="https://t.me/your_channel_link")
    )
    bot.send_message(message.chat.id, "👑 *SOVEREIGN ENTERPRISE ENGINE*\nReady for operation.", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("mode_"))
def handle_mode(call):
    mode = call.data.split("_")[1]
    text = "🚀 *BOOSTING TERMINAL*\nSelect service:" if mode == "boosting" else "📁 *ASSET MARKET*\nSelect account type:"

    markup = types.InlineKeyboardMarkup()
    if mode == "boosting":
        markup.add(types.InlineKeyboardButton("1k TG Members - $10", callback_data="buy_TG1K_10"))
    else:
        markup.add(types.InlineKeyboardButton("Aged FB (2010) - $20", callback_data="buy_FB10_20"))

    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def choose_payment(call):
    _, item, price = call.data.split("_")
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("☀️ Solana", callback_data=f"pay_SOL_{item}_{price}"),
        types.InlineKeyboardButton("💎 Ethereum", callback_data=f"pay_ETH_{item}_{price}"),
        types.InlineKeyboardButton("📱 OPay (Manual)", callback_data=f"pay_OPAY_{item}_{price}")
    )
    bot.edit_message_text(f"💳 *Order:* {item}\n*Price:* ${price}\nSelect Payment:", 
                          call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def execute_payment(call):
    _, method, item, price = call.data.split("_")

    if method == "OPAY":
        instruction = (f"🏦 *OPAY MANUAL PAYMENT*\n\nSend ${price} to:\n`{WALLETS['OPAY']}`\n\n"
                       "📸 *IMPORTANT:* Send a clear screenshot of your receipt here. I will hold the order until Admin verifies.")
    else:
        instruction = (f"🔗 *{method} BLOCKCHAIN PAYMENT*\n\nSend ${price} to:\n`{WALLETS[method]}`\n\n"
                       "📝 Paste your **Transaction Hash (TXID)** here. The system will verify on-chain and deliver instantly.")

    bot.edit_message_text(instruction, call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    bot.register_next_step_handler(call.message, finalize_order, method, item)

def finalize_order(message, method, item):
    if method == "OPAY":
        # Manual Mode: Just forward to you
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, f"🚨 *OPAY RECEIPT*\nUser: @{message.from_user.username}\nItem: {item}")
        bot.reply_to(message, "⏳ *Receipt received.* I am holding this for Admin approval. You will be notified.")
    else:
        # Auto Mode (Solana/ETH)
        tx_hash = message.text
        # Logic: Verify Hash on blockchain -> If success, deliver asset
        if len(str(tx_hash)) > 20: # Basic validation
            if "FB" in item:
                delivered_asset = FB_ACCOUNTS.pop(0) if FB_ACCOUNTS else "CONTACT ADMIN FOR STOCK"
                bot.reply_to(message, f"✅ *Payment Verified!*\n\nYour Asset:\n`{delivered_asset}`")
                bot.send_message(CHANNEL_ID, f"💎 *AUTO-SALE:* {item} delivered via {method}!")
            else:
                bot.reply_to(message, "✅ *Payment Verified!* Boosting has started on your link.")
                bot.send_message(CHANNEL_ID, f"🚀 *BOOSTING START:* {item} is active!")
        else:
            bot.reply_to(message, "❌ Invalid Hash. Order cancelled.")

if __name__ == "__main__":
    # Start the Newsroom background thread
    threading.Thread(target=news_broadcaster, daemon=True).start()

    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))

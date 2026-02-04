import os
import threading
from flask import Flask
from dotenv import load_dotenv
import telebot
from telebot import types
import requests

# 1. SETUP & CONFIG
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
SIM_TOKEN = os.getenv('SIM_TOKEN')
PORT = int(os.getenv('PORT', 5000))

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Render Health Check
@app.route('/')
def health_check():
    return "Bot is running and healthy!", 200

# 2. STOCK HELPERS
def get_stock_item(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        lines = f.readlines()
    if not lines:
        return None
    item = lines[0].strip()
    with open(filename, "w") as f:
        f.writelines(lines[1:])
    return item

# 3. BOT COMMANDS
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📱 Buy WhatsApp", callback_data="buy_wa")
    btn2 = types.InlineKeyboardButton("👤 Buy FB Account", callback_data="buy_fb")
    btn3 = types.InlineKeyboardButton("🔐 Buy VPN", callback_data="buy_vpn")
    btn4 = types.InlineKeyboardButton("💰 Check Balance", callback_data="check_bal")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        f"🔥 *Welcome to USA SMS BOT* 🔥\n\nSelect a service below to start.",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user = call.from_user

    if call.data == "buy_fb":
        item = get_stock_item("fb_stock.txt")
        if not item:
            bot.answer_callback_query(call.id, "❌ Out of stock!")
            return
        send_payment_info(call.message, "Facebook Account", item)

    elif call.data == "buy_vpn":
        item = get_stock_item("vpn_stock.txt")
        if not item:
            bot.answer_callback_query(call.id, "❌ Out of stock!")
            return
        send_payment_info(call.message, "VPN Key", item)

    elif call.data.startswith("paid_"):
        product = call.data.split("_")[1]
        # Notify Admin & Channel
        msg = (f"🚨 *PAYMENT CLAIMED*\n\n"
               f"👤 User: @{user.username} (`{user.id}`)\n"
               f"📦 Product: {product}\n"
               f"💳 Method: Opay/Solana\n\n"
               f"Check your accounts now!")
        bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")
        bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        bot.edit_message_text("✅ *Request Sent!*\nAdmin is verifying your payment. Your item will be sent shortly.", 
                              call.message.chat.id, call.message.message_id, parse_mode="Markdown")

def send_payment_info(message, product_name, item_reserved):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ I HAVE PAID", callback_data=f"paid_{product_name}"))

    pay_text = (
        f"🛒 *Order: {product_name}*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💵 *Opay Account:* `{os.getenv('OPAY_ACCOUNT')}`\n"
        f"👤 *Name:* {os.getenv('OPAY_NAME')}\n"
        f"🌐 *Solana:* `{os.getenv('SOL_WALLET')}`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚠️ Pay exactly and click the button below. Item reserved: `{item_reserved[:5]}...`"
    )
    bot.send_message(message.chat.id, pay_text, parse_mode="Markdown", reply_markup=markup)

# 4. RUNNER
def run_flask():
    app.run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    # Start Web Server in thread
    threading.Thread(target=run_flask).start()
    print("🚀 Web server started. Starting Bot polling...")
    # Start Bot
    bot.infinity_polling()


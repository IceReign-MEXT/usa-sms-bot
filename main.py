import os
import telebot
import requests
import time
from telebot import types
from flask import Flask
from threading import Thread

# --- INITIAL CONFIG ---
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID', '7033049440')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
ADMIN_USER = os.environ.get('ADMIN_USERNAME', '@Lona_trit')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER FOR RENDER ---
@app.route('/')
def home():
    return "Sovereign Store is Online", 200

# --- 5SIM API LOGIC ---
def buy_5sim_number(product):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    url = f'https://5sim.net/v1/user/buy/activation/usa/any/{product}'
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print(f"5SIM Error: {e}")
        return None

def check_5sim_sms(order_id):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    try:
        r = requests.get(f'https://5sim.net/v1/user/check/{order_id}', headers=headers)
        return r.json().get('sms')
    except:
        return None

# --- STOCK FILE LOGIC ---
def get_stock_item(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        lines = f.readlines()
    if not lines:
        return None
    item = lines[0].strip()
    with open(filename, "w") as f:
        f.writelines(lines[1:]) # Removes the item from the file
    return item

# --- BOT COMMANDS ---
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop Services", "💳 Deposit")
    kb.add("👤 My Profile", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Store* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop Services")
def shop(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_wa"),
        types.InlineKeyboardButton("📲 Telegram USA - $12", callback_data="buy_tg"),
        types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"),
        types.InlineKeyboardButton("📸 Instagram Account - $12", callback_data="buy_ig")
    )
    bot.send_message(m.chat.id, "🛒 *Select a product to buy:*", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(m):
    msg = f"💳 *PAYMENT DETAILS*\n\n🏦 OPAY: `{os.environ.get('OPAY_ACCOUNT', '7066549677')}`\n👤 Name: {os.environ.get('OPAY_NAME', 'Chisom Emmanuel')}\n\n📸 *Send a screenshot of your receipt here!*"
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_receipt(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Approve WhatsApp", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Approve Telegram", callback_data=f"ap_tg_{m.chat.id}"))
    kb.add(types.InlineKeyboardButton("✅ Approve Facebook", callback_data=f"ap_fb_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Approve Instagram", callback_data=f"ap_ig_{m.chat.id}"))
    kb.add(types.InlineKeyboardButton("❌ Reject Payment", callback_data=f"rej_{m.chat.id}"))

    bot.send_message(ADMIN_ID, f"📩 *New Receipt from @{m.from_user.username}*")
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "Check your Opay and select product to release:", reply_markup=kb)
    bot.send_message(m.chat.id, "⌛ *Payment sent to Admin for verification!* Please wait.")

# --- ORDER HANDLING ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split('_')
    action = data[0]

    if action == "buy":
        product = data[1]
        bot.send_message(call.message.chat.id, f"To buy {product.upper()}, click 'Deposit', pay, and upload your receipt!")

    elif action == "ap":
        product = data[1]
        user_id = data[2]

        # 1. HANDLE AUTOMATED NUMBERS (5SIM)
        if product in ["wa", "tg"]:
            service_name = "whatsapp" if product == "wa" else "telegram"
            bot.send_message(user_id, "🚀 *Payment Verified!* Searching for your USA number...")
            res = buy_5sim_number(service_name)

            if res and 'phone' in res:
                bot.send_message(user_id, f"✅ *Number Found!*\n\nPhone: `{res['phone']}`\n\n*Enter this into your app now.* Waiting for SMS...")
                # Loop to check SMS for 3 minutes
                for _ in range(18):
                    time.sleep(10)
                    sms = check_5sim_sms(res['id'])
                    if sms:
                        bot.send_message(user_id, f"📩 *YOUR CODE:* `{sms[0]['code']}`")
                        if CHANNEL_ID: bot.send_message(CHANNEL_ID, f"🔥 *NEW SALE:* USA {service_name.upper()} Delivered!")
                        return
                bot.send_message(user_id, "❌ SMS timed out. Contact @Lona_trit for a refund or retry.")
            else:
                bot.send_message(user_id, "❌ Error getting number. Admin will contact you.")
                bot.send_message(ADMIN_ID, f"⚠️ 5SIM ERROR for {user_id}. Check balance!")

        # 2. HANDLE AUTOMATED ACCOUNTS (STOCK FILE)
        elif product in ["fb", "ig"]:
            stock_file = "fb_stock.txt" if product == "fb" else "ig_stock.txt"
            account = get_stock_item(stock_file)

            if account:
                bot.send_message(user_id, f"✅ *Payment Verified!*\n\nHere is your account login:\n`{account}`")
                if CHANNEL_ID: bot.send_message(CHANNEL_ID, f"🔥 *NEW SALE:* {product.upper()} Account Delivered!")
            else:
                bot.send_message(user_id, "❌ Stock is currently empty! Admin @Lona_trit will send it manually.")
                bot.send_message(ADMIN_ID, f"⚠️ STOCK EMPTY for {product.upper()}! Send it manually to {user_id}.")

    elif action == "rej":
        bot.send_message(data[1], "❌ *Payment Rejected.* Please contact @Lona_trit.")
        bot.edit_message_text("❌ Payment Rejected.", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text == "📞 Support")
def support(m):
    bot.send_message(m.chat.id, f"Contact Owner: {ADMIN_USER}")

# --- STARTUP ---
def run_app():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run_app).start()
    print("Sovereign Bot Polling...")
    bot.infinity_polling()

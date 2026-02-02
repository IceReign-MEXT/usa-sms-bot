import os, telebot, requests, time
from telebot import types
from flask import Flask
from threading import Thread

# Config
TOKEN = os.environ.get('BOT_TOKEN')
SIM_TOKEN = os.environ.get('SIM_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.environ.get('CHANNEL_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Sovereign Shop Live", 200

# 5SIM BUY LOGIC
def buy_num(prod):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    r = requests.get(f'https://5sim.net/v1/user/buy/activation/usa/any/{prod}', headers=headers)
    return r.json()

def check_sms(oid):
    headers = {'Authorization': f'Bearer {SIM_TOKEN}', 'Accept': 'application/json'}
    r = requests.get(f'https://5sim.net/v1/user/check/{oid}', headers=headers)
    return r.json().get('sms')

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛍 Shop", "💳 Deposit", "📞 Support")
    bot.send_message(m.chat.id, "🐺 *Sovereign V15 Shop* 🐺\n\nAutomated USA Numbers & Aged Accounts.", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🛍 Shop")
def shop(m):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("📲 WhatsApp USA - $10", callback_data="buy_whatsapp"),
           types.InlineKeyboardButton("📲 Telegram USA - $12", callback_data="buy_telegram"),
           types.InlineKeyboardButton("👤 Facebook Aged - $15", callback_data="buy_fb"))
    bot.send_message(m.chat.id, "🛒 *Select Service:*", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💳 Deposit")
def deposit(m):
    bot.send_message(m.chat.id, f"💳 *Payment Detail*\n\n🏦 OPAY: \n\n📸 Send receipt screenshot here!")

@bot.message_handler(content_types=['photo'])
def receipt(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Approve WA", callback_data=f"ap_wa_{m.chat.id}"),
           types.InlineKeyboardButton("✅ Approve FB", callback_data=f"ap_fb_{m.chat.id}"),
           types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{m.chat.id}"))
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, "New Receipt! Select product to release:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    data = call.data.split('_')
    uid = data[2] if len(data) > 2 else None
    
    if data[0] == "ap" and data[1] == "wa":
        # Automated 5SIM purchase
        res = buy_num("whatsapp")
        if 'phone' in res:
            bot.send_message(uid, f"✅ *Approved!*\n\nYour Number: \n\nWaiting for SMS code...")
            # Wait for SMS
            for _ in range(10):
                time.sleep(15)
                sms = check_sms(res['id'])
                if sms:
                    bot.send_message(uid, f"📩 *CODE:* ")
                    if CHANNEL_ID: bot.send_message(CHANNEL_ID, "🔥 *NEW SALE:* USA WhatsApp Delivered!")
                    return
        else:
            bot.send_message(ADMIN_ID, "❌ 5SIM Error: Check balance or Token.")

    elif data[0] == "ap" and data[1] == "fb":
        bot.send_message(uid, "✅ *Approved!*\n\nPlease wait, Admin is sending your Facebook login...")
        bot.send_message(ADMIN_ID, f"User {uid} paid for FB. Send them the login now!")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))).start()
    bot.infinity_polling()

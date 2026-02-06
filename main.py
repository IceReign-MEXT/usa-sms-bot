
import os
import telebot
from telebot import types
from flask import Flask, request

app = Flask(__name__)

# --- CONFIG ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7033049440
CHANNEL_ID = -1002622160373

# Payment Details
SOL_ADDR = "B3iSYFxnm7cNmZvzdcKVD96kcycByuscgAFxSzPZBYFk"
OPAY_ACC = "7066549677 (Opay)"

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- INVENTORY DATA ---
MARKET_INVENTORY = {
    "fb_1yr": {"name": "🛡️ Facebook (1yr Aged)", "price": 5.0, "stock": 42},
    "fb_5yr": {"name": "👑 Facebook (5yr Elite)", "price": 15.0, "stock": 12},
    "tg_acc": {"name": "✈️ Telegram Aged Account", "price": 8.0, "stock": 15},
    "wa_acc": {"name": "🟢 WhatsApp High-Trust", "price": 12.0, "stock": 8}
}

SMM_SERVICES = {
    "s1": {"name": "📸 Instagram Followers", "rate": 1.2},
    "s2": {"name": "🧵 Facebook Page Likes", "rate": 0.95},
    "s3": {"name": "✈️ Telegram Members", "rate": 2.1}
}

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Market", "🚀 SMM Boost", "💳 My Wallet", "📰 Newsroom")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👑 *SOVEREIGN EMPIRE V5.0*\nDigital Asset Terminal & SMM Automation Active.", 
                     parse_mode='Markdown', reply_markup=main_menu())

# --- 🛒 AUTOMATED MARKET (ASSETS) ---
@bot.message_handler(func=lambda m: m.text == "🛒 Market")
def market_menu(m):
    markup = types.InlineKeyboardMarkup()
    text = "💎 *DIGITAL ASSET INVENTORY*\nSelect an item to purchase:\n\n"
    for key, item in MARKET_INVENTORY.items():
        text += f"• {item['name']} — `${item['price']}`\n"
        markup.add(types.InlineKeyboardButton(f"Buy {item['name']}", callback_data=f"buy_{key}"))
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_purchase(call):
    item_key = call.data.split("_")[1]
    item = MARKET_INVENTORY[item_key]
    bot.answer_callback_query(call.id)

    # Generate Invoice Text
    invoice = (f"🛡️ *INVOICE GENERATED*\n"
               f"━━━━━━━━━━━━━━\n"
               f"Asset: {item['name']}\n"
               f"Cost: `${item['price']}`\n\n"
               f"📍 SOL: `{SOL_ADDR}`\n"
               f"📍 CASH: `{OPAY_ACC}`\n\n"
               "Select payment method below:")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Paid Crypto (Verify)", callback_data=f"verify_{item_key}"))
    markup.add(types.InlineKeyboardButton("💸 Paid Cash (Notify Admin)", callback_data=f"cash_notify_{item_key}"))
    bot.send_message(call.message.chat.id, invoice, parse_mode='Markdown', reply_markup=markup)

# --- 🚀 AUTOMATED SMM (BOOSTING) ---
@bot.message_handler(func=lambda m: m.text == "🚀 SMM Boost")
def smm_menu(m):
    markup = types.InlineKeyboardMarkup()
    text = "🚀 *SMM BOOSTING ENGINES*\nSelect service to calculate price:\n"
    for sid, data in SMM_SERVICES.items():
        markup.add(types.InlineKeyboardButton(f"{data['name']} (${data['rate']}/1k)", callback_data=f"calc_{sid}"))
    bot.send_message(m.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("calc_"))
def smm_calc(call):
    sid = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, "🔢 *Enter Quantity:*")
    bot.register_next_step_handler(msg, process_smm_price, sid)

def process_smm_price(m, sid):
    try:
        qty = int(m.text)
        total = (qty / 1000) * SMM_SERVICES[sid]['rate']
        msg = bot.send_message(m.chat.id, f"💰 *Price: ${total:.2f}*\n\nPaste your Target Link:")
        bot.register_next_step_handler(msg, process_smm_final, sid, total, qty)
    except: bot.send_message(m.chat.id, "❌ Invalid Number.")

def process_smm_final(m, sid, total, qty):
    link = m.text
    invoice = (f"🛡️ *SMM ORDER INVOICE*\n"
               f"━━━━━━━━━━━━━━\n"
               f"Service: {SMM_SERVICES[sid]['name']}\n"
               f"Price: `${total:.2f}`\n\n"
               f"📍 SOL: `{SOL_ADDR}`\n"
               f"📍 CASH: `{OPAY_ACC}`\n\n"
               "Choose payment method:")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Verify Crypto", callback_data=f"v_smm_{total}"))
    markup.add(types.InlineKeyboardButton("💸 Notify Admin (Cash)", callback_data=f"c_smm_{total}"))
    bot.send_message(m.chat.id, invoice, parse_mode='Markdown', reply_markup=markup)

# --- NOTIFICATION SYSTEM ---
@bot.callback_query_handler(func=lambda call: "notify" in call.data or call.data.startswith("c_"))
def admin_notification(call):
    # This notifies your Private Channel and Admin ID
    bot.send_message(ADMIN_ID, f"🔔 *NEW CASH REQUEST*\nUser: {call.from_user.id}\nData: {call.data}")
    bot.send_message(CHANNEL_ID, f"📊 *Live Activity:* User `{call.from_user.id}` is completing a purchase.")
    bot.edit_message_text("✅ Admin notified. Waiting for cash confirmation.", call.message.chat.id, call.message.message_id)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

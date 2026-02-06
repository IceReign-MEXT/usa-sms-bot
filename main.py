import telebot
from telebot import types
import os
from flask import Flask, request

# --- CONFIGURATION ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
# Render automatically provides the internal port, we use the external URL for Webhooks
RENDER_URL = "https://usa-sms-bot-bgdj.onrender.com" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- INVENTORY DATA ---
ASSETS = {
    "facebook": {
        "Aged (2010-2015)": {"price": 15, "stock": 12, "desc": "High trust, fully warmed."},
        "Business Manager": {"price": 25, "stock": 5, "desc": "Verified BM, ready for ads."},
        "New Accounts": {"price": 5, "stock": 50, "desc": "Fresh accounts, phone verified."}
    },
    "smm": {
        "1k IG Followers": {"price": 10, "stock": "Unlimited", "desc": "Instant delivery, no drop."},
        "1k TG Members": {"price": 12, "stock": "Unlimited", "desc": "High quality real members."},
        "Post Likes/Views": {"price": 2, "stock": "Unlimited", "desc": "Global engagement boost."}
    }
}

@app.route('/')
def index():
    return "Sovereign Engine V10.1 Online", 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# --- BOT LOGIC ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Market (Assets)", callback_data="market"),
        types.InlineKeyboardButton("⚡ SMM Boosting", callback_data="smm"),
        types.InlineKeyboardButton("📞 Contact Admin", url=f"tg://user?id={ADMIN_ID}")
    )
    bot.reply_to(message, "👑 *SOVEREIGN EMPIRE V10.1*\nAsset Terminal Active.", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["market", "smm"])
def show_category(call):
    category = "facebook" if call.data == "market" else "smm"
    markup = types.InlineKeyboardMarkup()
    for item, data in ASSETS[category].items():
        markup.add(types.InlineKeyboardButton(f"{item} - ${data['price']}", callback_data=f"buy_{item}"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text="🔥 *Select Item:*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def purchase_flow(call):
    item_name = call.data.split("buy_")[1]
    item_data = ASSETS['facebook'].get(item_name) or ASSETS['smm'].get(item_name)

    text = (f"💎 *Order:* {item_name}\n💰 *Price:* ${item_data['price']}\n\n"
            "💳 *USDT (ERC20):*\n`0x742d35Cc6634C0532925a3b844Bc454e4438f44e`\n\n"
            "Click below after sending payment.")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ PAID (NOTIFY)", callback_data=f"paid_{item_name}"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("paid_"))
def verify_payment(call):
    item_name = call.data.split("paid_")[1]
    bot.send_message(ADMIN_ID, f"🚨 *PAYMENT:* {call.from_user.first_name} for {item_name}")
    bot.send_message(CHANNEL_ID, f"📈 *NEW ORDER:* {item_name} in progress...")
    bot.answer_callback_query(call.id, "Admin notified!", show_alert=True)

if __name__ == "__main__":
    # Remove old webhook and set the new one
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

    # Use gunicorn for production, but app.run for local testing
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))

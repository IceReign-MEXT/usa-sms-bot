import telebot
from telebot import types
import os
import time
from flask import Flask, request

# --- CONFIGURATION ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7033049440'))
CHANNEL_ID = os.getenv('CHANNEL_ID', '-1002622160373')
PORT = int(os.getenv('PORT', '8000'))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- INVENTORY DATA (V10) ---
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

# --- FLASK ROUTES (KEEP ALIVE) ---
@app.route('/')
def index():
    return "Sovereign Engine V10 is Active", 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# --- BOT LOGIC ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Market (Assets)", callback_data="market"),
        types.InlineKeyboardButton("⚡ SMM Boosting", callback_data="smm"),
        types.InlineKeyboardButton("📞 Contact Admin", url=f"tg://user?id={ADMIN_ID}"),
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/SovereignEmpireLogs")
    )

    welcome_text = (
        "👑 *Welcome to Sovereign Empire V10*\n\n"
        "The most advanced automated market for Aged Assets & SMM Boosting.\n\n"
        "✅ *Fast Delivery*\n"
        "✅ *Aged Accounts (2010+)*\n"
        "✅ *24/7 Automation*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["market", "smm"])
def show_category(call):
    category = "facebook" if call.data == "market" else "smm"
    markup = types.InlineKeyboardMarkup()

    for item, data in ASSETS[category].items():
        markup.add(types.InlineKeyboardButton(f"{item} - ${data['price']}", callback_data=f"buy_{item}"))

    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="back_start"))

    text = "🔥 *Available Inventory:*" if category == "facebook" else "⚡ *SMM Boosting Services:*"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def purchase_flow(call):
    item_name = call.data.split("buy_")[1]
    # Search in both categories
    item_data = ASSETS['facebook'].get(item_name) or ASSETS['smm'].get(item_name)

    if not item_data:
        bot.answer_callback_query(call.id, "Item not found.")
        return

    payment_text = (
        f"💎 *Order:* {item_name}\n"
        f"💰 *Price:* ${item_data['price']}\n"
        f"📝 *Details:* {item_data['desc']}\n\n"
        "💳 *Payment Address (USDT-ERC20/BTC):*\n"
        "`0x742d35Cc6634C0532925a3b844Bc454e4438f44e` (Tap to copy)\n\n"
        "⚠️ *After payment, click the button below to notify Admin.*"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ I HAVE PAID (CASH)", callback_data=f"paid_{item_name}"))
    markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="market"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text=payment_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("paid_"))
def verify_payment(call):
    item_name = call.data.split("paid_")[1]
    user = call.from_user

    # Notify Admin
    admin_alert = (
        "🚨 *NEW PAYMENT ALERT*\n\n"
        f"👤 *User:* {user.first_name} (@{user.username})\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"📦 *Item:* {item_name}\n\n"
        "Verify the transaction on the blockchain now."
    )
    bot.send_message(ADMIN_ID, admin_alert, parse_mode="Markdown")

    # Broadcast to Channel (Marketing Hype)
    channel_alert = (
        "📈 *LIVE ORDER IN PROGRESS*\n"
        "--- --- --- --- --- ---\n"
        f"👤 User: {user.first_name[0]}***\n"
        f"📦 Asset: {item_name}\n"
        "✅ Status: Waiting for Confirmation\n"
        "--- --- --- --- --- ---\n"
        "🛒 @SovereignEmpireBot"
    )
    bot.send_message(CHANNEL_ID, channel_alert, parse_mode="Markdown")

    # Confirm to User
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text="💎 *Payment Received!* Your request is being verified by the Sovereign Engine. Wait for 5-10 minutes.", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_start")
def back_to_start(call):
    welcome(call.message)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-app-name.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=PORT)

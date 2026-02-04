import os
import threading
from flask import Flask
from dotenv import load_dotenv
import telebot
from telebot import types

# 1. SETUP & CONFIG
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Render Health Check (This stops the "No open ports detected" error)
@app.route('/')
def health_check():
    return "Bot is active", 200

# 2. STOCK LOGIC
def get_stock(filename):
    if not os.path.exists(filename): return None
    with open(filename, "r") as f:
        lines = f.readlines()
    if not lines: return None
    item = lines[0].strip()
    with open(filename, "w") as f:
        f.writelines(lines[1:])
    return item

# 3. BOT HANDLERS
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 Buy WhatsApp", callback_data="buy_wa"))
    markup.add(types.InlineKeyboardButton("👤 Buy FB Account", callback_data="buy_fb"))
    bot.send_message(message.chat.id, "🚀 *USA SMS BOT READY*", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "buy_fb":
        item = get_stock("fb_stock.txt")
        if not item:
            bot.answer_callback_query(call.id, "❌ Out of Stock")
            return

        pay_msg = (f"💳 *Payment for FB Account*\n\n"
                  f"Opay: `{os.getenv('OPAY_ACCOUNT')}`\n"
                  f"Name: {os.getenv('OPAY_NAME')}\n\n"
                  f"Click below after paying.")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ I HAVE PAID", callback_data="confirm_pay"))
        bot.send_message(call.message.chat.id, pay_msg, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "confirm_pay":
        user = call.from_user
        alert = f"💰 *PAYMENT ALERT*\nUser: @{user.username}\nID: `{user.id}`"
        bot.send_message(CHANNEL_ID, alert, parse_mode="Markdown")
        bot.edit_message_text("⌛ Verifying... Admin will contact you.", call.message.chat.id, call.message.message_id)

# 4. STARTING THE ENGINE
def run_bot():
    bot.infinity_polling()

# This part is key: It starts the bot in a separate thread
# so the Web Server (Flask) can stay open for Render.
thread = threading.Thread(target=run_bot)
thread.start()

if __name__ == "__main__":
    # This is for local testing
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


import os
import requests
from flask import Flask, request
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SMM_API_KEY = os.environ.get("SMM_API_KEY")
SMM_API_URL = "https://morethanpanel.com/api/v2"

# Initialize Telegram Application
tb_app = Application.builder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_markdown(
        "👑 **Sovereign Guard V1.5 Active**\n\n"
        "📈 `/boost [ServiceID] [Link] [Qty]`\n"
        "💰 `/balance` - Check funds\n"
        "📊 `/status [OrderID]` - Check order"
    )

async def balance(update, context):
    payload = {'key': SMM_API_KEY, 'action': 'balance'}
    try:
        r = requests.post(SMM_API_URL, data=payload).json()
        await update.message.reply_text(f"💰 Balance: ${r.get('balance', '0.00')}")
    except:
        await update.message.reply_text("❌ Connection Error")

async def boost(update, context):
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /boost [ID] [Link] [Qty]")
        return
    payload = {
        'key': SMM_API_KEY, 'action': 'add',
        'service': context.args[0], 'link': context.args[1], 'quantity': context.args[2]
    }
    r = requests.post(SMM_API_URL, data=payload).json()
    if "order" in r:
        await update.message.reply_text(f"✅ Order ID: {r['order']}")
    else:
        await update.message.reply_text(f"❌ Error: {r.get('error')}")

tb_app.add_handler(CommandHandler("start", start))
tb_app.add_handler(CommandHandler("balance", balance))
tb_app.add_handler(CommandHandler("boost", boost))

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), tb_app.bot)
    await tb_app.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return "Bot Online"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
import logging
import json
import asyncio

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))  # Render назначает PORT

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# Хэндлеры
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Выберите категорию:\n🛠 Техподдержка\n🧑‍💻 IT Вопрос")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user
    log_entry = {"user": user.username, "text": message}
    with open("messages.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    await update.message.reply_text("✅ Заявка получена.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "ok"

@app.route("/")
def index():
    return "PraktikBot is running."

if __name__ == "__main__":
    # Устанавливаем webhook на Render-домен
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    asyncio.get_event_loop().run_until_complete(application.bot.set_webhook(webhook_url))
    app.run(host="0.0.0.0", port=PORT)

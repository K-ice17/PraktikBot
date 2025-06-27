import os
import json
import logging
import asyncio
from flask import Flask, request

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Flask-приложение
app = Flask(__name__)

# Получение токена и порта из переменных окружения
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# Инициализация Telegram Application
application = Application.builder().token(TOKEN).build()

# Хэндлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите категорию заявки:\n📌 Обучение\n💻 IT Вопросы"
    )

# Хэндлер текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    log_entry = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "text": message,
    }

    with open("messages.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    await update.message.reply_text("✅ Заявка получена, спасибо!")

# Регистрация хэндлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "ok", 200

# Простой healthcheck
@app.route("/", methods=["GET"])
def index():
    return "PraktikBot is running!", 200

# Запуск приложения
if __name__ == "__main__":
    # Установка webhook
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    asyncio.get_event_loop().run_until_complete(application.bot.set_webhook(webhook_url))
    app.run(host="0.0.0.0", port=PORT)

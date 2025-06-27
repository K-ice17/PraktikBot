import os
import json
import logging
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

# Переменные окружения
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# Создание Telegram-приложения
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите категорию заявки:\n📌 Обучение\n💻 IT Вопросы"
    )

# Обработчик обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    log = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "text": text,
    }

    with open("messages.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    await update.message.reply_text("✅ Заявка получена, спасибо!")

# Добавляем обработчики в приложение
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask маршруты
@app.route("/", methods=["GET"])
def index():
    return "PraktikBot работает", 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
async def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return "ok", 200

# Запуск приложения
if __name__ == "__main__":
    import asyncio

    async def main():
        # Устанавливаем Webhook
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{TOKEN}"
        await application.bot.set_webhook(webhook_url)

        # Запускаем Flask
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())

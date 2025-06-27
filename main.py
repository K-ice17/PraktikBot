from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import logging
import os
import json

TOKEN = os.getenv("TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

application = Application.builder().token(TOKEN).build()
app = Flask(__name__)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для логирования заявок. Выберите категорию:\n🛠 Техподдержка\n🧑‍💻 IT Вопрос")

# Обработка текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user
    log_entry = {
        "user": user.username,
        "text": message,
    }
    with open("messages.log", "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    await update.message.reply_text("✅ Заявка получена.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask endpoint для webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

if __name__ == "__main__":
    application.run_polling()

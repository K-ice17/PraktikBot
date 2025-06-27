import logging
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, Dispatcher, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN", "7809040819:AAHOVWb_dnv6kgdWOHdEFJ7cid5CZx_amAs")
LOG_FILE = "messages.log"

bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите категорию:\n"
        "🧹 Клининг\n💻 IT \n📄 Предоставить документ"
    )

# Обработка всех сообщений и логирование
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    log_entry = f"{user.first_name} (@{user.username}) [{user.id}]: {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    await update.message.reply_text("Спасибо! Ваша заявка принята.")

# Обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/")
def home():
    return "✅ Бот работает!"

if __name__ == "__main__":
    app.run(port=5000)

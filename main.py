import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN", "7809040819:AAHOVWb_dnv6kgdWOHdEFJ7cid5CZx_amAs")

app = Flask(__name__)

# Создание Telegram-приложения (бота)
application = Application.builder().token(TOKEN).build()

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите категорию:\n"
        "🧹 Клининг\n💻 IT Вопросы\n📄 Пожелания"
    )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Сохраняем сообщения в лог-файл
    with open("messages.log", "a", encoding="utf-8") as f:
        f.write(f"{user.first_name} (@{user.username}) [{user.id}]: {text}\n")

    await update.message.reply_text("Спасибо! Ваша заявка получена.")

# Обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Проверка работы сервиса
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

# Запуск Flask
if __name__ == "__main__":
    app.run(port=5000)

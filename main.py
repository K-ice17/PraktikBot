import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен
TOKEN = os.environ.get("TOKEN", "7809040819:AAHOVWb_dnv6kgdWOHdEFJ7cid5CZx_amAs")

bot = Bot(token=TOKEN)
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите категорию:\n"
        "🧹 Клининг\n💻 IT Вопросы\n📄 Предоставить документ"
    )

# Обработка всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Логируем в файл
    with open("messages.log", "a", encoding="utf-8") as f:
        f.write(f"{user.first_name} (@{user.username}) [{user.id}]: {text}\n")

    await update.message.reply_text("Спасибо! Ваша заявка принята.")

# Подключаем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Обработка Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

# Запуск на локальном сервере (Render сам запускает)
if __name__ == "__main__":
    app.run(port=5000)

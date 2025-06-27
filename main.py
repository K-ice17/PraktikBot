import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, Updater
import asyncio

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable not set")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /start")
    keyboard = [[InlineKeyboardButton("Оставить заявку", callback_data="submit")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже:", reply_markup=reply_markup)

# Обработчик кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получено нажатие на кнопку")
    query = update.callback_query
    await query.answer()

    if query.data == "submit":
        user = query.from_user
        logger.info(f"Получена заявка от @{user.username} (ID: {user.id})")
        await query.edit_message_text("✅ Заявка получена! Спасибо!")

# Запуск бота
async def main():
    logger.info("🟢 Бот запускается...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Вручную запускаем бота без вызова run_polling()
    await app.initialize()
    await app.updater.start_polling()
    await app.start()

    # Ждём завершения (например, по сигналу)
    try:
        while True:
            await asyncio.sleep(3600)  # Работаем вечно
    except (KeyboardInterrupt, SystemExit):
        logger.info("🔴 Бот останавливается...")
        await app.updater.stop()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())

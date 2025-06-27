import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

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
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

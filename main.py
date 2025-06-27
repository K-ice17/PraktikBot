import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from aiohttp import web

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Переменные окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", "8000"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-bot.onrender.com/webhook

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получена команда /start")
    keyboard = [[InlineKeyboardButton("Оставить заявку", callback_data="submit")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Получено нажатие на кнопку")
    query = update.callback_query
    await query.answer()
    if query.data == "submit":
        user = query.from_user
        logger.info(f"Получена заявка от @{user.username} (ID: {user.id})")
        await query.edit_message_text("✅ Заявка получена! Спасибо!")

# Вебхук
async def webhook_handler(request):
    try:
        update = Update.de_json(await request.json(), app.bot)
        await app.process_update(update)
        return web.Response()
    except Exception as e:
        logger.error(f"Ошибка в обработке вебхука: {e}")
        return web.Response(status=500)

# Настройка бота
async def setup_bot():
    logger.info("🟢 Бот запускается...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    await app.initialize()
    return app

# Запуск сервера
async def start_server():
    app_runner = web.AppRunner(app_web)
    await app_runner.setup()
    site = web.TCPSite(app_runner, host='0.0.0.0', port=PORT)
    logger.info(f"🚀 Сервер запущен на порту {PORT}")
    await site.start()

# Основной запуск
if __name__ == "__main__":
    import asyncio
    from telegram.ext import Application
    from aiohttp import web

    # Инициализируем бота
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(setup_bot())

    # Создаём веб-приложение
    app_web = web.Application()
    app_web.router.add_post("/webhook", webhook_handler)

    # Запускаем сервер
    loop.run_until_complete(start_server())
    loop.run_forever()

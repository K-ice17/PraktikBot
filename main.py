import os
from datetime import datetime
from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup

TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable not set")

bot = Bot(token=TOKEN)

app = Flask(__name__)

# Хранение выбранной темы для каждого пользователя (chat_id)
user_categories = {}

# Клавиатура с категориями
keyboard = [['🧹 Клининг'], ['💻 IT'], ['📄 Предоставить документ']]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def send_to_sheets(user_id, category, text):
    # TODO: Реализовать отправку данных в Google Sheets
    pass

def send_to_group(user_id, category, text):
    # TODO: Реализовать пересылку сообщений в Telegram-группу
    pass

@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    if not update.message or update.message.text is None:
        return 'OK'
    chat_id = update.message.chat.id
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    username = user.username or ''
    # Логирование сообщения в файл
    with open('messages.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {user_id} - {username} - {text}\n")
    # Обработка команды /start
    if text == '/start':
        user_categories[chat_id] = None
        bot.send_message(chat_id=chat_id, text="Пожалуйста, выберите тему:", reply_markup=reply_markup)
    elif text in ['🧹 Клининг', '💻 IT', '📄 Предоставить документ']:
        # Пользователь выбрал категорию
        user_categories[chat_id] = text
        bot.send_message(chat_id=chat_id, text=f"Вы выбрали тему \"{text}\". Отправьте текстовое сообщение по этой теме.")
    else:
        # Обычное текстовое сообщение
        category = user_categories.get(chat_id)
        if category:
            # Обработка сообщения с выбранной категорией
            send_to_sheets(user_id, category, text)
            send_to_group(user_id, category, text)
            bot.send_message(chat_id=chat_id, text="Спасибо! Ваше сообщение получено.")
            user_categories[chat_id] = None
        else:
            bot.send_message(chat_id=chat_id, text="Пожалуйста, выберите тему, нажав на кнопку ниже.", reply_markup=reply_markup)
    return 'OK'

if __name__ == '__main__':
    # Установка webhook на Render
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        webhook_url = f"{render_url}/{TOKEN}"
        bot.set_webhook(webhook_url)
    else:
        hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
        if hostname:
            webhook_url = f"https://{hostname}/{TOKEN}"
            bot.set_webhook(webhook_url)
    # Запуск Flask-сервера
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

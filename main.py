import telebot
from datetime import datetime
import time

# НАСТРОЙКИ - ВСТАВЬТЕ СВОИ ДАННЫЕ
TOKEN = '8703704685:AAG1gnukxZURXf3H-1NHfZkr8ZyGnDLr-64'
YOUR_CHAT_ID = 8056677771

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Для статистики
scan_stats = {
    'total': 0,
    'today': 0,
    'users': set(),
    'last_scan': None
}

current_date = datetime.now().strftime("%Y-%m-%d")

@bot.message_handler(commands=['start'])
def handle_start(message):
    global scan_stats, current_date
    
    today = datetime.now().strftime("%Y-%m-%d")
    if today != current_date:
        current_date = today
        scan_stats['today'] = 0

    user = message.from_user
    args = message.text.split()
    source = "🔵 QR-код" if len(args) > 1 and args[1] == "qr" else "⚪ Прямая ссылка"
    scan_time = datetime.now().strftime("%H:%M:%S")

    scan_stats['total'] += 1
    scan_stats['today'] += 1
    scan_stats['users'].add(user.id)

    # Уведомление вам
    notification = f"🔔 СКАНИРОВАНИЕ!\n{source}\n👤 {user.first_name}\n📊 Всего: {scan_stats['total']}"
    try:
        bot.send_message(YOUR_CHAT_ID, notification)
    except:
        pass

    # Ответ пользователю
    bot.send_message(message.chat.id, f"👋 Привет, {user.first_name}!\n✅ Спасибо за сканирование!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.from_user.id == YOUR_CHAT_ID:
        bot.send_message(message.chat.id, "✅ Ок")
    else:
        bot.send_message(message.chat.id, "Отправь /start")

if __name__ == "__main__":
    print("🤖 БОТ ЗАПУЩЕН!")
    print(f"👤 Владелец ID: {YOUR_CHAT_ID}")
    print("📢 Ожидание сканирований...")
    bot.infinity_polling()

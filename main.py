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

# Текущая дата для подсчета "сегодня"
current_date = datetime.now().strftime("%Y-%m-%d")

@bot.message_handler(commands=['start'])
def handle_start(message):
    global scan_stats, current_date

    # Проверяем, не изменилась ли дата
    today = datetime.now().strftime("%Y-%m-%d")
    if today != current_date:
        current_date = today
        scan_stats['today'] = 0

    # Получаем информацию о пользователе
    user = message.from_user
    user_info = (
        f"👤 Имя: {user.first_name} {user.last_name or ''}\n"
        f"🆔 ID: {user.id}\n"
        f"📱 Username: @{user.username or 'нет'}\n"
        f"🌐 Язык: {user.language_code or 'ru'}"
    )

    # Проверяем, откуда пришел пользователь (по QR или нет)
    args = message.text.split()
    source = "🔵 QR-код" if len(args) > 1 and args[1] == "qr" else "⚪ Прямая ссылка"

    # Время сканирования
    scan_time = datetime.now().strftime("%H:%M:%S")

    # Обновляем статистику
    scan_stats['total'] += 1
    scan_stats['today'] += 1
    scan_stats['users'].add(user.id)
    scan_stats['last_scan'] = f"{today} {scan_time}"

    # КРАСИВОЕ УВЕДОМЛЕНИЕ ДЛЯ ВАС (точно как вы показали)
    notification = (
        "🔔 **НОВОЕ СКАНИРОВАНИЕ QR!**\n"
        "═══════════════════════\n"
        f"{source}\n"
        f"⏰ Время: {today} {scan_time}\n"
        f"{user_info}\n"
        "═══════════════════════\n"
        f"📊 Статистика:\n"
        f"   • Всего: {scan_stats['total']}\n"
        f"   • Сегодня: {scan_stats['today']}\n"
        f"   • Уникальных: {len(scan_stats['users'])}"
    )

    # Отправляем уведомление ВАМ
    try:
        bot.send_message(YOUR_CHAT_ID, notification, parse_mode='Markdown')
        print(f"✅ Уведомление отправлено владельцу в {scan_time}")
    except Exception as e:
        print(f"❌ Ошибка отправки уведомления: {e}")

    # Отвечаем пользователю, который отсканировал QR
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"✨ Спасибо за сканирование!\n"
        f"📊 Вы {scan_stats['total']}-й посетитель\n\n"
        f"💬 Чем я могу помочь?"
    )

    bot.send_message(message.chat.id, welcome_text)

    # Логируем в консоль
    print(f"\n[{scan_time}] {source}")
    print(f"   Пользователь: @{user.username or 'нет'} ({user.first_name})")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    """Показывает статистику (только для владельца)"""
    if message.from_user.id == YOUR_CHAT_ID:
        stats_text = (
            "📊 **СТАТИСТИКА БОТА**\n"
            "══════════════════\n"
            f"📈 Всего сканирований: {scan_stats['total']}\n"
            f"📅 Сегодня: {scan_stats['today']}\n"
            f"👥 Уникальных пользователей: {len(scan_stats['users'])}\n"
            f"🕐 Последнее: {scan_stats['last_scan'] or 'нет'}"
        )
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Эта команда только для владельца")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Отвечает на любые сообщения"""
    if message.from_user.id == YOUR_CHAT_ID:
        bot.send_message(message.chat.id, "✅ Команда получена (владелец)")
    else:
        responses = [
            "Интересно... Расскажи подробнее!",
            "Я тебя слушаю 👂",
            "Хорошо, что ты написал!",
            "Задай мне вопрос"
        ]
        import random
        bot.send_message(message.chat.id, random.choice(responses))

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 БОТ @Banali_bot ЗАПУЩЕН!")
    print("=" * 50)
    print(f"👤 Владелец ID: {YOUR_CHAT_ID}")
    print(f"⏰ Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print("📢 Ожидание сканирований...")
    print("❌ Нажмите Ctrl+C для остановки")
    print("=" * 50)

    bot.infinity_polling()

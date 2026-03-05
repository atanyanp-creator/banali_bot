import qrcode
from PIL import Image

# Данные вашего бота
BOT_USERNAME = "Banali_bot"  # Имя вашего бота

# Создаем ссылку на бота
qr_link = f"https://t.me/{BOT_USERNAME}?start=qr"

# Настраиваем QR-код
qr = qrcode.QRCode(
    version=5,  # Размер (чем больше, тем детальнее)
    box_size=15,  # Размер одного квадратика
    border=3,  # Толщина рамки
    error_correction=qrcode.constants.ERROR_CORRECT_H  # Высокая надежность
)

qr.add_data(qr_link)
qr.make(fit=True)

# Создаем изображение
img = qr.make_image(fill_color="black", back_color="white")

# Сохраняем
filename = f"qr_{BOT_USERNAME}.png"
img.save(filename)

print("=" * 50)
print("✅ QR-код создан!")
print("=" * 50)
print(f"📱 Имя бота: @{BOT_USERNAME}")
print(f"🔗 Ссылка в QR: {qr_link}")
print(f"🖼 Файл: {filename}")
print("=" * 50)
print("\n🎯 Этот QR-код можно:")
print("   • Распечатать на визитках")
print("   • Вставить в презентацию")
print("   • Наклеить на товары")
print("   • Отправить друзьям")
print("=" * 50)
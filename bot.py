import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton
)

TOKEN = os.getenv("BOT_TOKEN")
# ВСТАВЬ СВОЙ TELEGRAM ID (число), чтобы получать уведомления о заявках
ADMIN_ID = 123456789  

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

# Главное меню (Reply-кнопки внизу экрана)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Получить гайд"), KeyboardButton(text="❓ Частые вопросы")],
        [KeyboardButton(text="📩 Оставить заявку / Связаться")]
    ],
    resize_keyboard=True
)

# Inline-кнопка для ссылки
guide_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Скачать гайд (PDF)", url="https://google.com")]
    ]
)

# Inline-меню для FAQ
faq_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💰 Сколько стоят услуги?", callback_data="faq_price")],
        [InlineKeyboardButton(text="⏱ Сроки выполнения?", callback_data="faq_time")],
        [InlineKeyboardButton(text="🚀 Как начать работу?", callback_data="faq_start")]
    ]
)

# --- ХЭНДЛЕРЫ ---

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    welcome_text = (
        f"Здравствуйте, {message.from_user.first_name}! 👋\n\n"
        "Я официальный бот-помощник.\n"
        "Здесь вы можете скачать полезный гайд, узнать ответы на популярные вопросы "
        "или оставить заявку на консультацию."
    )
    await message.answer(welcome_text, reply_markup=main_kb)

@dp.message(F.text == "📖 Получить гайд")
async def send_guide(message: types.Message):
    await message.answer(
        "Ваш гайд готов к скачиванию! Жмите на кнопку ниже 👇", 
        reply_markup=guide_inline_kb
    )
    # Уведомление админу
    if ADMIN_ID != 123456789:
        await bot.send_message(
            ADMIN_ID, 
            f"🔔 Пользователь @{message.from_user.username or message.from_user.id} скачал гайд!"
        )

@dp.message(F.text == "❓ Частые вопросы")
async def show_faq(message: types.Message):
    await message.answer("Выберите интересующий вас вопрос:", reply_markup=faq_inline_kb)

# Обработка нажатий на FAQ
@dp.callback_query(F.data.startswith("faq_"))
async def process_faq(callback: types.CallbackQuery):
    if callback.data == "faq_price":
        await callback.message.answer("💳 Стоимость рассчитывается индивидуально под ваш проект.")
    elif callback.data == "faq_time":
        await callback.message.answer("⏱ В среднем разработка и запуск занимают от 1 до 3 дней.")
    elif callback.data == "faq_start":
        await callback.message.answer("🚀 Для старта просто нажмите кнопку «Оставить заявку» в меню!")
    await callback.answer()

@dp.message(F.text == "📩 Оставить заявку / Связаться")
async def lead_request(message: types.Message):
    await message.answer("Спасибо за проявленный интерес! Менеджер свяжется с вами в ближайшее время.")
    
    # Отправка заявки тебе в личку
    if ADMIN_ID != 123456789:
        user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        await bot.send_message(
            ADMIN_ID, 
            f"🚀 **НОВАЯ ЗАЯВКА!**\nОт: {message.from_user.full_name} ({user_info})"
        )

# Обработка любого другого текста
@dp.message(F.text)
async def fallback_handler(message: types.Message):
    await message.answer(
        "Воспользуйтесь кнопками меню ниже, чтобы найти нужную информацию 👇", 
        reply_markup=main_kb
    )

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

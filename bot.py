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
# Вставь свой ID от @userinfobot (число без кавычек), чтобы получать заявки
ADMIN_ID = 123456789  

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КЛАВИАТУРЫ ---

# 1. Главное меню (внизу экрана)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Забрать гайд"), KeyboardButton(text="🧮 Рассчитать стоимость")],
        [KeyboardButton(text="❓ Частые вопросы"), KeyboardButton(text="🚀 Заказать услугу")]
    ],
    resize_keyboard=True
)

# 2. Кнопка выдачи гайда
guide_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📖 Открыть гайд (PDF)", url="https://google.com")]
    ]
)

# 3. Интерактивный калькулятор
calc_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Лендинг / Сайт", callback_data="calc_site")],
        [InlineKeyboardButton(text="🤖 Telegram-бот", callback_data="calc_bot")],
        [InlineKeyboardButton(text="📈 Продвижение / Реклама", callback_data="calc_promo")]
    ]
)

# 4. Меню FAQ
faq_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⏱ Сроки разработки", callback_data="faq_time")],
        [InlineKeyboardButton(text="💳 Способы оплаты", callback_data="faq_pay")]
    ]
)

# --- ХЭНДЛЕРЫ ---

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    welcome_text = (
        f"Здравствуйте, **{message.from_user.first_name}**! 👋\n\n"
        "Добро пожаловать в сервис автоматических услуг.\n\n"
        "Воспользуйтесь меню ниже, чтобы скачать гайд, рассчитать "
        "стоимость вашего проекта или связаться со специалистом 👇"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_kb)

# Выдача гайда
@dp.message(F.text == "🎁 Забрать гайд")
async def send_guide(message: types.Message):
    guide_text = (
        "🔥 **Ваш пошаговый гайд готов!**\n\n"
        "Внутри собраны лучшие практики по развитию бизнеса и автоматизации "
        "процессов. Нажимайте на кнопку ниже:"
    )
    await message.answer(guide_text, parse_mode="Markdown", reply_markup=guide_kb)

# Калькулятор
@dp.message(F.text == "🧮 Рассчитать стоимость")
async def show_calculator(message: types.Message):
    await message.answer("Выберите тип проекта для расчета примерной стоимости:", reply_markup=calc_kb)

@dp.callback_query(F.data.startswith("calc_"))
async def process_calc(callback: types.CallbackQuery):
    if callback.data == "calc_site":
        ans = "💻 **Разработка сайта:** от 15 000 ₽\n⏱ Сроки: 3–5 дней."
    elif callback.data == "calc_bot":
        ans = "🤖 **Разработка Telegram-бота:** от 10 000 ₽\n⏱ Сроки: 1–3 дня."
    elif callback.data == "calc_promo":
        ans = "📈 **Настройка рекламы:** от 20 000 ₽\n⏱ Сроки: от 7 дней."
    
    await callback.message.answer(ans, parse_mode="Markdown")
    await callback.answer()

# FAQ
@dp.message(F.text == "❓ Частые вопросы")
async def show_faq(message: types.Message):
    await message.answer("Ответы на популярные вопросы:", reply_markup=faq_kb)

@dp.callback_query(F.data.startswith("faq_"))
async def process_faq(callback: types.CallbackQuery):
    if callback.data == "faq_time":
        ans = "⏱ Большинство задач мы выполняем за **24–72 часа**."
    elif callback.data == "faq_pay":
        ans = "💳 Работаем по предоплате 50% (карты, перевод, крипта)."
    
    await callback.message.answer(ans, parse_mode="Markdown")
    await callback.answer()

# Сбор заявок (Заказать услугу)
@dp.message(F.text == "🚀 Заказать услугу")
async def lead_request(message: types.Message):
    await message.answer(
        "✅ **Заявка принята!**\nМенеджер свяжется с вами в течение 15 минут.",
        parse_mode="Markdown"
    )
    
    # Отправка уведомления тебе в личку
    if ADMIN_ID != 123456789:
        user_info = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        await bot.send_message(
            ADMIN_ID,
            f"🔔 **НОВАЯ ЗАЯВКА НА УСЛУГУ!**\n\n"
            f"**Клиент:** {message.from_user.full_name}\n"
            f"**Контакт:** {user_info}"
        )

async def main():
    print("Профессиональный бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопка со ссылкой на ваш гайд (замените ссылку на свою)
guide_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📖 Открыть гайд", url="https://google.com")]
    ]
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Жми на кнопку ниже, чтобы забрать свой гайд.\n"
        "Если у тебя есть вопросы — просто напиши их мне в чат!"
    )
    await message.answer(welcome_text, reply_markup=guide_keyboard)

@dp.message(F.text)
async def handle_questions(message: types.Message):
    user_text = message.text.lower()
    
    # Шаблонные ответы на частые вопросы (FAQ)
    if "цена" in user_text or "стоимость" in user_text:
        await message.answer("💰 Наши услуги абсолютно бесплатны!")
    elif "как" in user_text or "гайд" in user_text:
        await message.answer("Жми на кнопку в самом первом сообщении, чтобы открыть материал!", reply_markup=guide_keyboard)
    else:
        await message.answer("Спасибо за вопрос! Наш специалист скоро свяжется с вами.")

async def main():
    print("Бот успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from src.workflow import app
from src.utils.states import GlobalState

# ====== Настройки ======
API_TOKEN = "ТВОЙ_ТОКЕН_БОТА"  # получи у @BotFather
logging.basicConfig(level=logging.INFO)

# ====== Инициализация ======
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ====== Хэндлеры ======

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет 👋 Я лингво-бот. Напиши мне предложение или тему для курса!")


@dp.message()
async def handle_message(message: types.Message):
    user_input = message.text.strip()

    # Оборачиваем в GlobalState
    state = GlobalState(query=user_input, logs=[])

    # Прогоняем через workflow
    result = app.invoke(state)

    # Если это проверка грамматики
    if hasattr(result, "grammar_result"):
        await message.answer(f"✍️ Проверка грамматики:\n\n{result.grammar_result}")
        return

    # Если это курс
    if hasattr(result, "course"):
        course = result.course
        text = (
            "📚 *Мини-курс готов!*\n\n"
            f"*Введение:*\n{course.get('Введение', '—')}\n\n"
            f"*Практика:*\n{course.get('Практика', '—')}\n\n"
            f"*Доп. материалы:*\n{course.get('Доп. материалы', '—')}\n"
        )
        await message.answer(text, parse_mode="Markdown")
        return

    # Если что-то пошло не так
    await message.answer("😅 Не смог обработать запрос. Попробуй ещё раз!")


# ====== Запуск ======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

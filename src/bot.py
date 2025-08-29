import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

from src.workflow import app
from src.utils.states import GlobalState

# ====== Настройки ======
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
logging.basicConfig(level=logging.INFO)

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")

# ====== Инициализация ======
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# ====== Хэндлеры ======

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет 👋 Я лингво-бот. Напиши тему или предложение — соберу конспект, тесты и видео.")


@dp.message()
async def handle_message(message: types.Message):
    user_input = (message.text or "").strip()
    if not user_input:
        await message.answer("Похоже, сообщение пустое. Напиши тему для обучения ✍️")
        return

    # Сбор состояния и запуск воркфлоу
    state = GlobalState(query=user_input)
    result = app.invoke(state)

    # Предпочитаем собранный курс, если он сформирован воркфлоу
    if getattr(result, "course", None):
        course = result.course or {}
        parts = []
        summary_text = (course.get("summary") or result.summarize or "—").strip()
        if summary_text and summary_text != "—":
            parts.append("📘 Конспект\n\n" + summary_text)

        tests = course.get("tests") or result.test or []
        if isinstance(tests, list) and tests:
            preview = []
            for item in tests[:3]:
                q = item.get("question") if isinstance(item, dict) else None
                if q:
                    preview.append(f"• {q}")
            if preview:
                parts.append("📝 Тесты (пример)\n\n" + "\n".join(preview))

        videos = course.get("videos") or result.youtube or []
        if isinstance(videos, list) and videos:
            links = [f"- {link}" for link in videos]
            parts.append("▶️ Видео\n\n" + "\n".join(links))

        text = "\n\n".join(parts) if parts else "Не удалось собрать материалы по теме. Попробуйте переформулировать запрос."
        await message.answer(text)
        return

    # Если курс не сформирован, отправляем то, что есть по частям
    sent_any = False

    if getattr(result, "summarize", None):
        await message.answer("📘 Конспект\n\n" + result.summarize)
        sent_any = True

    if getattr(result, "test", None):
        tests = result.test or []
        if isinstance(tests, list) and tests:
            preview = []
            for item in tests[:3]:
                q = item.get("question") if isinstance(item, dict) else None
                if q:
                    preview.append(f"• {q}")
            if preview:
                await message.answer("📝 Тесты (пример)\n\n" + "\n".join(preview))
                sent_any = True

    if getattr(result, "youtube", None):
        videos = result.youtube or []
        if isinstance(videos, list) and videos:
            links = [f"- {link}" for link in videos]
            await message.answer("▶️ Видео\n\n" + "\n".join(links))
            sent_any = True

    if not sent_any:
        await message.answer("😅 Не смог обработать запрос. Попробуйте ещё раз!")


# ====== Запуск ======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

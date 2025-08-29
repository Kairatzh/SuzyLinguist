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
logger = logging.getLogger("bot")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Переменная окружения TELEGRAM_BOT_TOKEN не установлена.")

# ====== Инициализация ======
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# ====== Утилиты отправки ======
MAX_MESSAGE_LEN = 4000  # запас до лимита Telegram ~4096

async def send_text(chat_id: int, text: str) -> None:
    if not text:
        return
    if len(text) <= MAX_MESSAGE_LEN:
        await bot.send_message(chat_id, text)
        return
    start = 0
    while start < len(text):
        chunk = text[start:start + MAX_MESSAGE_LEN]
        await bot.send_message(chat_id, chunk)
        start += MAX_MESSAGE_LEN

# ====== Хэндлеры ======

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет 👋 Я лингво-бот. Напиши тему или предложение — соберу конспект, тесты и видео.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Я помогу собрать мини-курс по теме:\n\n"
        "1) Конспект по теме\n"
        "2) Превью тестов\n"
        "3) Ссылки на видео\n\n"
        "Просто отправь мне тему (например: 'Article usage in English')."
    )


@dp.message()
async def handle_message(message: types.Message):
    user_input = (message.text or "").strip()
    if not user_input:
        await message.answer("Похоже, сообщение пустое. Напиши тему для обучения ✍️")
        return

    # Сбор состояния и запуск воркфлоу
    state = GlobalState(query=user_input)

    try:
        # выносим синхронный invoke в отдельный поток, чтобы не блокировать event loop
        result = await asyncio.to_thread(app.invoke, state)
    except Exception as e:
        logger.exception("invoke failed: %s", e)
        await message.answer("Внутренняя ошибка при обработке запроса. Попробуйте ещё раз позже.")
        return

    # Если форматирующая финальная стадия подготовила сборку (текст/файл) — отправляем её приоритетно
    final_text = getattr(result, "final_message", None)
    final_file = getattr(result, "final_file", None)
    if final_text or final_file:
        # Если есть файл (PDF), пробуем отправить как документ с подписью
        if final_file:
            try:
                await bot.send_document(message.chat.id, final_file, caption=final_text or None)
                return
            except Exception:
                # Если отправка файла не удалась — упадём назад к тексту
                pass
        if final_text:
            await send_text(message.chat.id, final_text)
            return

    # Предпочитаем собранный курс, если он сформирован воркфлоу (фоллбэк, когда finalizer не сработал)
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
        await send_text(message.chat.id, text)
        return

    # Если курс не сформирован, отправляем то, что есть по частям
    sent_any = False

    if getattr(result, "summarize", None):
        await send_text(message.chat.id, "📘 Конспект\n\n" + result.summarize)
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
                await send_text(message.chat.id, "📝 Тесты (пример)\n\n" + "\n".join(preview))
                sent_any = True

    if getattr(result, "youtube", None):
        videos = result.youtube or []
        if isinstance(videos, list) and videos:
            links = [f"- {link}" for link in videos]
            await send_text(message.chat.id, "▶️ Видео\n\n" + "\n".join(links))
            sent_any = True

    if not sent_any:
        await message.answer("😅 Не смог обработать запрос. Попробуйте ещё раз!")


# ====== Запуск ======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

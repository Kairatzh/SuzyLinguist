"""
    format.py:
        Форматируем текста
"""

import os
from aiogram.types import FSInputFile

from src.utils.states import GlobalState


def formatizer(state: GlobalState) -> GlobalState:
    """
    Финальная тулза:
    - Склеивает текст курса и PDF в одно сообщение.
    - Сохраняет в state.final_message и state.final_file.
    """
    try:
        course = getattr(state, "course", {})
        text_parts = [" *Мини-курс готов!*", ""]

        if "Введение" in course:
            text_parts.append("🔹 *Введение*")
            text_parts.append(course["Введение"])
            text_parts.append("")

        if "Практика" in course:
            text_parts.append("📝 *Практика*")
            text_parts.append(course["Практика"])
            text_parts.append("")

        if "Доп. материалы" in course:
            text_parts.append("🎥 *Доп. материалы*")
            text_parts.append(course["Доп. материалы"])
            text_parts.append("")

        final_text = "\n".join(text_parts)

        if hasattr(state, "pdf_path") and os.path.exists(state.pdf_path):
            state.final_message = final_text
            state.final_file = FSInputFile(state.pdf_path)
        else:
            state.final_message = final_text
            state.final_file = None

    except Exception as e:
        state.logs.append(f"[finalizer] Ошибка: {e}")

    return state

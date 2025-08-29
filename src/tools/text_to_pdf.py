import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.utils.states import GlobalState


def pdf_export(state: GlobalState) -> GlobalState:
    """
    Тулза: генерирует PDF из текста курса и сохраняет путь в state.pdf_path.
    """
    try:
        text = ""
        if hasattr(state, "course") and isinstance(state.course, dict):
            text += " Мини-курс\n\n"
            for section, content in state.course.items():
                if section == "Структура":
                    continue
                text += f"=== {section} ===\n{content}\n\n"
        else:
            text = getattr(state, "query", "Нет данных")

        filename = "course.pdf"
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        for line in text.split("\n"):
            if line.strip():
                elements.append(Paragraph(line, styles["Normal"]))
                elements.append(Spacer(1, 12))

        doc.build(elements)
        state.pdf_path = os.path.abspath(filename)

    except Exception as e:
        state.logs.append(f"[pdf_export] Ошибка: {e}")

    return state

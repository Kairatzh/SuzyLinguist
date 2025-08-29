"""
src/workflow.py:
Граф воркфлоу, который объединяет результаты всех тулз
в единый мини-курс перед завершением.
"""

from langchain_core.runnables import RunnableParallel
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import Runnable
from src.utils.states import GlobalState
from src.tools.grammar import grammar
from src.tools.summary import summarize
from src.tools.test import test_generate
from src.tools.youtube_search import find_video
from src.orchestrator import orchestrator


# ========================
# Узлы с обработкой ошибок
# ========================

def grammar_check(state: GlobalState) -> GlobalState:
    try:
        return grammar(state)
    except Exception as e:
        state.logs.append(f"[grammar_check] Ошибка: {e}")
        return state


def summary_step(state: GlobalState) -> GlobalState:
    try:
        return summarize(state)
    except Exception as e:
        state.logs.append(f"[summary_step] Ошибка: {e}")
        return state


def test_generation(state: GlobalState) -> GlobalState:
    try:
        return test_generate(state)
    except Exception as e:
        state.logs.append(f"[test_generation] Ошибка: {e}")
        return state


def youtube_search(state: GlobalState) -> GlobalState:
    try:
        return find_video(state)
    except Exception as e:
        state.logs.append(f"[youtube_search] Ошибка: {e}")
        return state


def hub_node(state: GlobalState) -> GlobalState:
    """Пустая нода-хаб для параллельного запуска тулз."""
    return state


def course_builder(state: GlobalState) -> GlobalState:
    """
    Объединяет результаты всех предыдущих тулз в
    структурированный мини-курс.
    """
    try:
        # Пример: соберем все в state.course
        state.course = {
            "summary": getattr(state, "summary", None),
            "tests": getattr(state, "tests", None),
            "videos": getattr(state, "videos", None),
            "structure": [
                "Введение (summary)",
                "Практика (tests)",
                "Доп. материалы (videos)"
            ]
        }
    except Exception as e:
        state.logs.append(f"[course_builder] Ошибка: {e}")
    return state


# ===========
# Построение графа
# ===========

workflow = StateGraph(GlobalState)

# Узлы
workflow.add_node("grammar_check", grammar_check)
workflow.add_node("hub_node", hub_node)
workflow.add_node("summary", summary_step)
workflow.add_node("test_generation", test_generation)
workflow.add_node("youtube_search", youtube_search)
workflow.add_node("course_builder", course_builder)

# Ветвление: orchestrator решает путь
workflow.add_conditional_edges(
    START,
    orchestrator,
    {
        "check": "grammar_check",
        "generate": "hub_node"
    }
)

# Ветка "check"
workflow.add_edge("grammar_check", END)

# Ветка "generate": hub_node → все тулзы → course_builder → END
workflow.add_edge("hub_node", "summary")
workflow.add_edge("hub_node", "test_generation")
workflow.add_edge("hub_node", "youtube_search")

workflow.add_edge("summary", "course_builder")
workflow.add_edge("test_generation", "course_builder")
workflow.add_edge("youtube_search", "course_builder")

workflow.add_edge("course_builder", END)

# Компилируем
app = workflow.compile()

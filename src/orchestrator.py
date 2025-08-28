"""
    src/orchestrator.py:
        Простой оркестратор-координатор, решающий какую ветку запускать.
        Возвращает метку маршрута для графа: "check" или "generate".
"""

from src.utils.states import GlobalState


def orchestrator(state: GlobalState) -> str:
    """Определяет, какую ветку запускать на основе текста запроса.

    Правила (минимально-достаточные для MVP):
    - Если в запросе есть слово "check" (в любом месте, регистронезависимо) — идём в грамматическую проверку.
    - Иначе — стандартная генерация мини-курса.
    """
    if not state or not state.query:
        return "generate"

    query_lower = state.query.lower()
    if "check" in query_lower:
        return "check"
    return "generate"



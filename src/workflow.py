"""
    src/workflow.py:
        Основная воркфлоу графа и компиляция его.
"""

from langgraph.graph import START, END, StateGraph

from src.utils.states import GlobalState
from src.tools.grammar import grammar
from src.tools.summary import summarize
from src.tools.test import test_generate
from src.tools.youtube_search import find_video
from src.orchestrator import orchestrator

def router(state: GlobalState):
    # Оставлено для совместимости, но в графе используется orchestrator
    if state.query and "check" in state.query.lower():
        return "check"
    return "generate"

def check(state: GlobalState) -> GlobalState:
    return grammar(state)

def generate(state: GlobalState) -> GlobalState:
    state = summarize(state)
    state = test_generate(state)
    state = find_video(state)
    return state

workflow = StateGraph(GlobalState)

workflow.add_node("summary", summarize)
workflow.add_node("test_generate", test_generate)
workflow.add_node("youtube_search", find_video)
workflow.add_node("check", check)
workflow.add_node("generate", generate)

workflow.add_conditional_edges(START, orchestrator, {
    "check": "check",
    "generate": "generate"
})
workflow.add_edge("check", END)
workflow.add_edge("generate", END)

app = workflow.compile()

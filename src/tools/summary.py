"""
    src/tools/summary.py:
        Получаем тему и выводим краткий конспект.
"""
from langchain_together import Together

from src.utils.configs.settings import load_configs
from src.utils.prompts import summary_prompt
from utils.states import GlobalState

configs = load_configs()
llm = Together(
    model=configs["llm"]["summarize_llm"]["model"],
    together_api_key=configs["llm"]["together_api_key"],
    temperature=configs["llm"]["summarize_llm"]["temperature"],
    max_tokens=configs["llm"]["summarize_llm"]["max_tokens"]
)
responce = llm | summary_prompt

def summmarize(state: GlobalState) -> GlobalState:
    query = state.query
    state.summarize = responce.invoke({"query": query})
    return state

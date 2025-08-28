"""
    src/tools/grammar.py:
        Получаем текст и проверяем на грамматические ошибки.Если есть то выводим подробную описание
"""


from langchain_together import Together

from src.utils.configs.settings import load_configs
from src.utils.prompts import grammar_prompt
from utils.states import GlobalState

configs = load_configs()
llm = Together(
    model=configs["llm"]["grammar_llm"]["model"],
    together_api_key=configs["llm"]["together_api_key"],
    temperature=configs["llm"]["grammar_llm"]["temperature"],
    max_tokens=configs["llm"]["grammar_llm"]["max_tokens"]
)
responce = llm | grammar_prompt

def grammar(state: GlobalState) -> GlobalState:
    query = state.query
    state.grammar = responce.invoke({"query": query})
    return state
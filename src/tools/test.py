"""
    src/tools/test.py:
        Получаем запрос и генерируем тесты для этой темы.
"""


from langchain_together import Together

from src.utils.configs.settings import load_configs
from src.utils.prompts import test_prompt
from utils.states import GlobalState

configs = load_configs()
llm = Together(
    model=configs["llm"]["test_llm"]["model"],
    together_api_key=configs["llm"]["together_api_key"],
    temperature=configs["llm"]["test_llm"]["temperature"],
    max_tokens=configs["llm"]["test_llm"]["max_tokens"]
)
responce = llm | test_prompt

def test_generate(state: GlobalState) -> GlobalState:
    query = state.query
    state.test = responce.invoke({"query": query})
    return state
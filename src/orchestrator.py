"""
    src/orchestrator.py:
        Простой оркестратор-координатор, решающий какую ветку запускать.
        Возвращает метку маршрута для графа: "check" или "generate".
"""

from itertools import chain
from src.utils.configs.settings import load_configs
from src.utils.states import GlobalState
from langchain_together import Together
from langchain_core.prompts import PromptTemplate

configs = load_configs()

prompt_template = """
Ты — оркестратор. Выбери режим:
- "check" → если запрос про исправление грамматики или ошибок.
- "generate" → если запрос про объяснения, курс, тесты или материалы.
Отвечай только одним словом: check или generate.
Запрос: {query}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["query"]
)
llm = Together(
    model=configs["llm"]["test_llm"]["model"],
    temperature=0,
    max_tokens=50,
    together_api_key=configs["llm"]["together_api_key"]
)
responce = prompt | llm

def orchestrator(state: GlobalState) -> str:
    query = state.query
    responce.invoke({"query": query})
    return responce

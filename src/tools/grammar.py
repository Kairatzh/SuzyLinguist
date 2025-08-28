"""
    src/tools/grammar.py:
        Получаем текст и проверяем на грамматические ошибки. 
        Если есть ошибки – даём краткий фидбэк и пример.
"""

from langchain_together import Together
from langchain_core.output_parsers import StrOutputParser

from src.utils.configs.settings import load_configs
from src.utils.prompts import grammar_prompt
from src.utils.states import GlobalState

configs = load_configs()

llm = Together(
    model=configs["llm"]["grammar_llm"]["model"],
    together_api_key=configs["llm"]["together_api_key"],
    temperature=configs["llm"]["grammar_llm"]["temperature"],
    max_tokens=configs["llm"]["grammar_llm"]["max_tokens"]
)

response_chain = grammar_prompt | llm | StrOutputParser()

def grammar(state: GlobalState) -> GlobalState:
    if not state.query:
        state.grammar = "No text provided."
        return state
    try:
        state.grammar = response_chain.invoke({"query": state.query})
    except Exception as e:
        state.grammar = f"Error during grammar check: {e}"
    return state

"""
    src/tools/test.py:
        Получаем запрос и генерируем тесты для этой темы.
"""

import json
from langchain_together import Together
from langchain_core.output_parsers import StrOutputParser

from src.utils.configs.settings import load_configs
from src.utils.prompts import test_prompt
from src.utils.states import GlobalState
from langchain_community.chat_models import ChatDeepInfra

llm = ChatDeepInfra(
    model="deepseek-ai/DeepSeek-V3.1",  # можно заменить на qwen, mixtral и т.д.
    temperature=0.7,
    deepinfra_api_token="IqErJHDEjwajUPQX6jAHo4Fmk96ZDLol"
)
configs = load_configs()
# llm = Together(
#     model=configs["llm"]["model"],
#     together_api_key=configs["llm"]["together_api_key"],
#     temperature=configs["llm"]["test_llm"]["temperature"],
#     max_tokens=configs["llm"]["test_llm"]["max_tokens"]
# )
response_chain = test_prompt | llm | StrOutputParser()

def test_generate(state: GlobalState) -> GlobalState:
    if not state.query:
        state.test = []
        return state

    try:
        tests_raw = response_chain.invoke({"query": state.query})
    except Exception:
        state.test = []
        return state

    try:
        test_dict = json.loads(tests_raw)
        state.test = test_dict
    except json.JSONDecodeError:
        state.test = []
    return state
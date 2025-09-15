"""
    src/tools/summary.py:
     Получаем тему и выводим краткий конспект.
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_together import Together

from src.utils.configs.settings import load_configs
from src.utils.prompts import summary_prompt
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
#     temperature=configs["llm"]["summarize_llm"]["temperature"],
#     max_tokens=configs["llm"]["summarize_llm"]["max_tokens"]
# )

# структурированный оутпут и готовый пайплайн
output = StrOutputParser() 
response_chain = summary_prompt | llm | output

def summarize(state: GlobalState) -> GlobalState:
    if not state.query:
        state.summarize = "No query provided."
        return state
    
    try:
        state.summarize = response_chain.invoke({"query": state.query})
    except Exception as e:
        state.summarize = f"Error during summarization: {e}"
    return state


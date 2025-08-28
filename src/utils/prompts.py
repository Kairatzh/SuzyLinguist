"""
    src/utils/prompts.py:
        Нужные промты хранятся тут и можно менять их удобно и быстро
"""
from langchain_core.prompts import PromptTemplate

# Summary prompt: {Text -> Text}
summary_prompt_template = ""
summary_prompt = PromptTemplate(
    input_variables=["query"],
    template=summary_prompt_template
)

# Test prompt: {Text -> Text}
test_prompt_template = ""
test_prompt = PromptTemplate(
    input_variables=["query"],
    template=test_prompt_template
)

"""
    src/utils/prompts.py:
        Нужные промты хранятся тут и можно менять их удобно и быстро
"""


from langchain_core.prompts import PromptTemplate


# Summary prompt: {Text -> Text}
summary_prompt_template = """
You are a professional linguistics and language teacher.  
Your task: generate a study summary in the **same language as the user’s query**.  

Topic: "{query}"  

Constraints:
- Output must be in the same language as the input.
- Maximum length: 500 tokens.
- Be precise, clear, and concise.
- No unnecessary introductions or filler text.

Structure the summary into sections:
1. Key Concepts (bullet points, max 5)
2. Explanation (short, focused paragraph, max 5 sentences)
3. Examples (2–3 short, clear examples)
4. Checklist for Learners (bullet list of 3–5 practical steps)

"""
summary_prompt = PromptTemplate(
    input_variables=["query"],
    template=summary_prompt_template
)

# Test prompt: {Text -> Json}
test_prompt_template = """
You are a professional language teacher and test creator.  
Your task: generate 10 test questions about the topic "{topic}" in the **same language as the input**.  

Constraints:
- Output must be in strict JSON format.
- Each question must have:
  - "question": the test question
  - "options": 4 answer choices (list)
  - "correct_answer": the right choice
- Keep questions short, clear, and precise.
- No explanations, no extra text outside JSON.

Example format:
[
  {
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "..."
  },
  ...
]
"""
test_prompt = PromptTemplate(
    input_variables=["query"],
    template=test_prompt_template
)

# Grammar prompt: {text -> text}
grammar_prompt_template = """
You are a professional language teacher and grammar corrector.  
Your task: check the grammar of the user’s text and respond in the **same language as the input**.  

Text: "{query}"

Constraints:
- Maximum length: 200 tokens.
- Be concise, clear, and practical.
- Provide only short feedback and one corrected version.
- Give 1 simple example for clarification.

Output structure:
1. Feedback (1–2 sentences about mistakes)
2. Corrected Text
3. Example Sentence (showing correct usage)
"""
grammar_prompt = PromptTemplate(
    input_variables=["query"],
    template=grammar_prompt_template
)

"""
    src/tools/speaking.py
        Получаем голос пользователя, проверяем с эталоном и выдаём фидбэк.
        Это в "TODO"
"""

import tempfile
from rapidfuzz import fuzz
from openai import OpenAI

from src.utils.states import GlobalState
from src.utils.configs.settings import load_configs

configs = load_configs()
client = OpenAI(api_key=configs["llm"]["openai_api_key"])

def check_speaking(state: GlobalState, audio_bytes: bytes, correct_text: str) -> GlobalState:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        audio_path = tmp.name

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    user_text = transcript.text.strip()

    score = fuzz.ratio(user_text.lower(), correct_text.lower())

    if score > 80:
        feedback = f"Отлично! Похоже на правильный ответ.\n\nВаш ответ: {user_text}"
    else:
        feedback = f"Есть ошибки.\n\nВаш ответ: {user_text}\nПравильный ответ: {correct_text}"

    state.grammar = feedback  
    return state

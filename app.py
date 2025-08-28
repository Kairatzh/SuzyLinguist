import streamlit as st

from src.workflow import app as graph_app
from src.utils.states import GlobalState


st.set_page_config(page_title="SuzyLinguist", page_icon="🗣️", layout="centered")

st.title("SuzyLinguist")
st.caption("ИИ-агент: конспект • тест • YouTube • проверка грамматики (по команде 'check')")

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_assistant_output(state: GlobalState):
    # Формируем компактный ответ
    parts = []
    if state.grammar:
        parts.append(f"Грамматика:\n{state.grammar}")
    if state.summarize:
        parts.append(f"Конспект:\n{state.summarize}")
    if state.test:
        parts.append("Тест (10 вопросов, JSON):\n" + ("```json\n" + str(state.test) + "\n```"))
    if state.youtube:
        yt = "\n".join(state.youtube)
        parts.append(f"YouTube:\n{yt}")
    return "\n\n".join(parts) if parts else "Нет данных."


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Введите тему или 'check <текст>' для проверки грамматики"):
    # Пользовательское сообщение
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Инференс графа
    state = GlobalState(query=prompt)
    result_state = graph_app.invoke(state)

    assistant_text = render_assistant_output(result_state)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    with st.chat_message("assistant"):
        st.markdown(assistant_text)



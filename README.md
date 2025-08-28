# SuzyLinguist
ИИ‑агент для генерации мини‑курсов: конспект, тесты, YouTube‑ссылки и проверка грамматики.

## Запуск (быстрый старт)

1) Установите зависимости:
```
pip install -r requirements.txt
```

2) Переменные окружения:
- `TOGETHER_API_KEY` — ключ Together AI (обязательно для LLM)
- `OPENAI_API_KEY` — опционально для speaking (пока не используется)

Можно положить их в `.env` (подхватится автоматически).

3) Запустите фронтенд (Streamlit):
```
streamlit run app.py
```

## Использование
- Введите тему (любой язык): получите конспект, 10 вопросов теста (JSON), 2–3 ссылки YouTube.
- Введите `check <текст>`: получите краткий фидбэк по грамматике, исправленный вариант и пример.

## Архитектура
- `src/workflow.py` — граф LangGraph, точки входа `check`/`generate`.
- `src/orchestrator.py` — логика выбора ветки.
- `src/tools/*.py` — инструменты: `summary`, `test`, `grammar`, `youtube_search`.
- `src/utils/prompts.py` — промпты.
- `src/utils/configs/config.yml` — конфиг моделей и токенов.


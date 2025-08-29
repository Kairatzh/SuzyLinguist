#  Suzy Linguist — Телеграм‑бот для изучения языков

**Suzy Linguist** — Telegram-бот на Python, который с помощью LLM генерирует краткий конспект по теме, тестовые вопросы и находит релевантные видео на YouTube. Оркестрация выполняется через LangGraph.

##  Возможности

- **Конспект**: краткое структурированное резюме по теме запроса
- **Тесты**: генерация набора вопросов (JSON), в боте показывается превью
- **Видео**: подбор нескольких ссылок с YouTube по теме

##  Быстрый старт

### Установка

```bash
git clone <repository-url>
cd SuzyLinguist
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install -r requirements.txt
```

### Конфигурация

1) Создайте `.env` в корне и добавьте ключи:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_BotFather
TOGETHER_API_KEY=ваш_together_api_key
```

2) Отредактируйте `src/utils/configs/config.yml` при необходимости (модель, лимиты токенов, температуры):

```yaml
llm:
  together_api_key: ${TOGETHER_API_KEY}
  model: "deepseek-ai/DeepSeek-V3"
  summarize_llm:
    max_tokens: 500
    temperature: 0.3
  test_llm:
    max_tokens: 600
    temperature: 0.4
```

### Запуск бота

```bash
python -m src.bot
```

Бот запускается в режиме long polling. Откройте диалог с вашим ботом в Telegram и отправьте тему, например: "Present Simple vs Present Continuous".

##  Архитектура

```
SuzyLinguist/
├── requirements.txt
├── README.md
└── src/
    ├── bot.py                 # Aiogram-бот, интеграция с воркфлоу
    ├── workflow.py            # LangGraph граф, собирает summary/tests/videos в course
    ├── tools/
    │   ├── summary.py         # Генерация конспекта (Together LLM)
    │   ├── test.py            # Генерация тестов (JSON через Together LLM)
    │   ├── youtube_search.py  # Поиск видео (youtube-search-python)
    │   └── speaking.py        # Черновик проверки произношения (TODO)
    └── utils/
        ├── states.py          # Pydantic-модель GlobalState
        ├── prompts.py         # PromptTemplate для summary/test
        ├── configs/
        │   ├── config.yml     # Конфиг LLM
        │   └── settings.py    # Загрузка конфига и .env
        └── logger.py          # Заготовка для логирования
```

Главные поля `GlobalState`:
- `query`: исходный запрос пользователя
- `summarize`: текст конспекта
- `test`: список вопросов (dict со свойствами `question`, `options`, `correct_answer`)
- `youtube`: список ссылок на видео
- `course`: агрегированная структура, которую формирует `workflow.course_builder`

##  Взаимодействие бота

`src/bot.py` загружает `TELEGRAM_BOT_TOKEN` из `.env`, принимает текстовые сообщения, запускает `app.invoke(state)` и отправляет:
- конспект (если есть),
- превью первых 2–3 тестовых вопросов,
- ссылки на видео. Если `course` сформирован воркфлоу — собирает эти части в единый ответ.

##  Зависимости

См. `requirements.txt`. Ключевые: `aiogram`, `langchain`, `langgraph`, `langchain-together`, `youtube-search-python`, `pydantic`, `python-dotenv`.

##  Лицензия

MIT — см. `LICENSE`.

---

**Suzy Linguist** — ваш ИИ-помощник в изучении языков в Telegram. 🧠✨


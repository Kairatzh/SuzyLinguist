"""
    src/tools/youtube_search.py:
        Получаем от пользователя тему и ищем через тулзы и в ответ получаем ссылку.
"""

from youtubesearchpython import VideosSearch
from src.utils.states import GlobalState

def find_video(state: GlobalState) -> GlobalState:
    videos = VideosSearch(state.query, limit=1).result()
    state.youtube = videos['result'][0]['link']
    return state

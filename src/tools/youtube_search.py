"""
    src/tools/youtube_search.py:
        Получаем от пользователя тему и ищем через YouTube, возвращаем ссылки.
"""

from youtubesearchpython import VideosSearch
from src.utils.states import GlobalState

def find_video(state: GlobalState) -> GlobalState:
    try:
        videos = VideosSearch(state.query, limit=3).result() 
        links = [v['link'] for v in videos.get('result', [])]
        state.youtube = links if links else None
    except Exception as e:
        state.youtube = None
    return state
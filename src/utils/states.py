"""
    src/utils/states.py:
        Модуль для хранения глобального состояния приложения.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict

class GlobalState(BaseModel):
    """Класс состояния, хранит все результаты работы агентов."""
    query: Optional[str] = None          
    youtube: Optional[List[str]] = None  
    test: Optional[List[Dict]] = None    
    summarize: Optional[str] = None      
    grammar: Optional[str] = None       

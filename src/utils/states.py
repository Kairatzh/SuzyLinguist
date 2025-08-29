"""
    src/utils/states.py:
        Модуль для хранения глобального состояния приложения.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class GlobalState(BaseModel):
    """Класс состояния, хранит все результаты работы агентов."""
    query: Optional[str] = None            
    youtube: Optional[List[str]] = None   
    test: Optional[List[Dict]] = None     
    summarize: Optional[str] = None       
    course: Optional[Dict[str, Any]] = None  
    pdf_path: Optional[str] = None         

    final_message: Optional[str] = None    
    final_file: Optional[Any] = None       

    logs: List[str] = []

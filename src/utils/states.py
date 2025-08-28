"""
    src/utils/states.py:
        Храним все состояние тут.
"""
import json
from pydantic import BaseModel
from typing import Optional, Literal

class GlobalState(BaseModel):
    query: Optional[str]
    youtube: Optional[str]
    test: Optional[str]
    summarize: Optional[str]
    grammar: Optional[str]


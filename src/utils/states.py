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
    test: Optional[json]
    summarize: Optional[str]

"""
    src/utils/configs/setting.py:
        НАСТРОЙКА LOAD_CONFIG ДЛЯ ОСТАЛЬНЫХ ФАЙЛОВ.УДОБНОЕ ИСПОЛЬЗОВАНИЕ КОНФИГОВ!
"""

import os.path

import yaml
from dotenv import load_dotenv

def load_configs(path="src/utils/configs/config.yml"):
    load_dotenv()
    with open(path, "r") as f:
        raw = f.read()
    resolved = os.path.expandvars(raw)
    return yaml.safe_load(resolved)
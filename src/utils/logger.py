"""
    src/utils/logger.py:
        удобноe логгирование в остальных файлах
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("SuzyLogger")

if __name__ == "__main__":
    logger.info("Приложение запустилось")
    logger.warning("Что-то пошло не так")
    logger.error("Ошибка в работе модуля")
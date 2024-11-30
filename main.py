from fastapi import FastAPI
from app.yc_log_handler import ycLogHandler
from app.app import app
import os, sys, json
from dotenv import load_dotenv

load_dotenv()

# Загрузка конфига
with open('config.json', 'r') as f:
    config = json.load(f)

# Уровень логирования
LOG_LEVEL = config.get("log_level", "INFO")

# Проверяем, запущено ли приложение на Vercel
log_type = os.getenv("LOG_TYPE", "volume")

# Настраиваем логирование
if log_type == "volume":
    # Логи записываются в файл
    from loguru import logger
    logger.remove()
    logger.add("logs/debug.log", format="{time} {level} {message}", level=LOG_LEVEL, rotation="100 MB")
elif log_type == "vercel":
    # Логи выводятся в консоль
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, format="{time} {level} {message}", level=LOG_LEVEL)
elif log_type == "yc":
    # Логи выводятся в консоль
    from app.log_config import logger

GITHUB_SHA = os.getenv("GITHUB_SHA", "unknown_version")
GITHUB_REF = os.getenv("GITHUB_REF", "unknown_branch")

main_app = FastAPI(
    title="OpenAI SDK Adapter",
    description="Adapter from OpenAI SDK to Yandex Cloud FoMo API",
    version=f"{GITHUB_SHA=} - {GITHUB_REF=}",
    logger=logger
)

main_app.include_router(app)

logger.info("My log message", extra={"my-key": "my-value"})

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:main_app", host="0.0.0.0", port=9041, reload=True)

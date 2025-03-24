import os
import sys

from loguru import logger

from app.common.constants import LOG_DIR_PATH
from app.common.enums import ProjectBuildTypes

from .settings import settings

if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH)

LOG_FILE = f"{LOG_DIR_PATH}/app.log"
LEVEL = "DEBUG" if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.PRODUCTION else "ERROR"

logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "format": "<cyan>{time:HH:mm:ss DD/MM/YYYY}</cyan> | <level>{level: <8}</level> | <level>{message}</level>",
            "level": LEVEL,
        }
    ]
)

logger.add(
    LOG_FILE,
    format="{time:HH:mm:ss DD/MM/YYYY} | {level} | {message}",
    rotation="10MB",
    retention="10 days",
    level=LEVEL,
    encoding="utf-8",
)

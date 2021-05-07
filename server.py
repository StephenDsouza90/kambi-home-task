import logging

from interface.interface import app
from utils.utils import initialize_logging


initialize_logging("logs/api.log", "kambi_home_task")

logger = logging.getLogger("kambi_home_task")
logger.info("Starting server")
logger.info("Listening at: http://127.0.0.1:8000")

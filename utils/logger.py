"""Simple logger wrapper."""
import logging

logger = logging.getLogger("ai_recommender")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_logger():
    """Return configured logger."""
    return logger

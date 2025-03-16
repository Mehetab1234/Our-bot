import logging
import sys

def setup_logger() -> logging.Logger:
    """Setup and return logger instance"""
    logger = logging.getLogger('discord_bot')
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(handler)
    return logger

import os
from typing import Dict

def load_config() -> Dict[str, str]:
    """Load configuration from environment variables"""
    return {
        'token': os.getenv('DISCORD_TOKEN', ''),
        'prefix': os.getenv('COMMAND_PREFIX', '!')
    }

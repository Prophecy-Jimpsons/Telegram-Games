import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

# Game Configuration
GAME_TIMEOUT = 60  # seconds
MAX_PLAYERS = 2

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'logs/telegram_games.log'

# UI Configuration
GAME_SYMBOLS = {
    'X': '❌',
    'O': '⭕',
    'EMPTY': '⬜',
    'SELECTED': '🔵',
    'WINNER': '🏆'
}

# Emoji Configuration
EMOJIS = {
    'GAME': '🎮',
    'DICE': '🎲',
    'TROPHY': '🏆',
    'CLOCK': '⏰',
    'WARNING': '⚠️',
    'ERROR': '❌',
    'SUCCESS': '✅',
    'WAITING': '⌛',
    'PLAYER': '👤',
    'ROBOT': '🤖'
}
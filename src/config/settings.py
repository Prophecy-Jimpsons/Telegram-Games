import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

# Game Settings
GAME_TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '60'))
MAX_PIECES_PER_PLAYER = 4
BOARD_SIZE = 4

# Webapp Settings
WEBAPP_URL = "https://jimpsons.org/tictactoe"
ALLOWED_ORIGINS = ["https://jimpsons.org"]


# TODO: Might need to remove inline bot sseeting
# Message Templates
MESSAGES = {
        'webapp_start': (
        "🎮 Welcome to 4x4 Tic-Tac-Toe! Testing Webapp popup from Python\n"
        "Click the button below to start playing:"
    ),
    'game_start': (
        "4x4 Tic-Tac-Toe!\n"
        "Player X: {x_name}\n"
        "Waiting for player O to join...\n"
        "Use /join to join the game!"
    ),
    'game_in_progress': "A game is already in progress in this chat!",
    'private_chat_error': "This game must be played in a group chat. Add me to a group and use /start there!",
    'no_game_exists': "No game in progress. Use /start to begin.",
    'game_is_full': "Game is full!",
    'cannot_play_self': "You can't play against yourself!",
    'not_your_turn': "Not your turn!",
    'space_occupied': "Space already occupied!",
    'timeout_win': (
        "⏰ Time's Up!\n\n"
        "Player {winner} ({winner_name}) wins by default!\n"
        "Player {loser} was inactive for too long.\n\n"
        "Use /start to begin a new game. 🎮"
    ),
    'help_text': """
4x4 Tic-Tac-Toe Game Rules:

1. Each player gets 4 pieces
2. First phase: Place all pieces
3. Second phase: Move any of your pieces
4. Win by getting:
   - Four in a row
   - Four in a column
   - Four in a diagonal
   - Four in a 2x2 square

Commands:
/start - Start a new game
/join - Join an existing game
/help - Show this help message
"""
}


from typing import List, Optional, Tuple
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from src.config.settings import WEBAPP_URL

def create_keyboard_with_highlight(
    board: List[List[str]],
    highlight_pos: Optional[Tuple[int, int]] = None,
    winning_pattern: Optional[List[Tuple[int, int]]] = None
) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard representing the game board.
    
    Args:
        board: The current game board state
        highlight_pos: Position to highlight (selected piece)
        winning_pattern: List of positions in winning pattern
    
    Returns:
        InlineKeyboardMarkup: The formatted keyboard
    """
    keyboard = []
    for i, row in enumerate(board):
        keyboard_row = []
        for j, cell in enumerate(row):
            if winning_pattern and (i, j) in winning_pattern:
                button_text = f"🏆{cell}🏆"
            elif (i, j) == highlight_pos:
                button_text = f"[{cell}]" if cell != " " else "[·]"
            else:
                button_text = cell if cell != " " else "·"
            keyboard_row.append(
                InlineKeyboardButton(button_text, callback_data=f"{i},{j}")
            )
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)


def create_game_start_keyboard():
    web_app = WebAppInfo(url=WEBAPP_URL)
    keyboard = [
        [InlineKeyboardButton("Play 4x4 Tic-Tac-Toe", web_app=web_app)],
        [InlineKeyboardButton("Join Game", callback_data="join_game")]
    ]
    return InlineKeyboardMarkup(keyboard)
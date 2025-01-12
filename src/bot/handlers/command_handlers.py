# src/bot/handlers/command_handlers.py
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import ContextTypes
from src.games.models.game_state import GameState
from src.utils.logger import logger
import traceback

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command - Launch the game WebApp"""
    try:
        # Explicitly create WebApp button
        web_app = WebAppInfo(url="https://jimpsons.org/tictactoe")
        
        keyboard = [[
            InlineKeyboardButton(
                text="🎮 Play 4x4 Tic-Tac-Toe", 
                web_app=web_app
            )
        ]]
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🎮 Welcome to 4x4 Tic-Tac-Toe!\n"
            "Click the button below to start playing:",
            reply_markup=reply_markup
        )
        
        logger.info(f"WebApp game initiated by user {update.effective_user.id}")

    except Exception as e:
        logger.error(f"WebApp button error: {e}")
        logger.error(traceback.format_exc())
        await update.message.reply_text(
            f"Sorry, there was an error starting the game: {str(e)}"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    help_text = """
*4x4 Tic-Tac-Toe Game Rules:*

1. Each player gets 4 pieces
2. First phase: Place all pieces
3. Second phase: Move any of your pieces
4. Win by getting:
   - Four in a row
   - Four in a column
   - Four in a diagonal
   - Four in a 2x2 square

*Commands:*
/start - Start a new game
/help - Show this help message
"""
    await update.message.reply_text(help_text, parse_mode='MarkdownV2')
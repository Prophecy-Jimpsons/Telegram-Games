from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import (
    TelegramError,
    Forbidden,
    BadRequest,
    TimedOut,
    NetworkError
)
from src.utils.logger import logger

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot."""
    try:
        error = context.error
        chat_id = update.effective_chat.id if update else None

        if isinstance(error, BadRequest) and "Button_type_invalid" in str(error):
            # Handle WebApp button error
            await context.bot.send_message(
                chat_id=chat_id,
                text="Sorry, there was an error starting the game. Please make sure you're using the latest version of Telegram."
            )
        elif isinstance(error, Forbidden):
            logger.error(f"Bot was blocked by user in chat {chat_id}")
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Sorry, something went wrong. Please try again."
            )

        logger.error(f"Update {update} caused error {error}")
    
    except Exception as e:
        logger.error(f"Error in error handler: {e}")
        
async def timeout_handler(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle game timeouts."""
    try:
        games_to_remove = []
        for chat_id, game in context.bot_data.get("games", {}).items():
            if game.phase not in ["finished", "waiting"]:
                winner = "O" if game.current_player == "X" else "X"
                try:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"⏰ Game timed out! Player {winner} ({game.player_names[winner]}) wins by default!"
                    )
                    games_to_remove.append(chat_id)
                except TelegramError as e:
                    logger.error(f"Error sending timeout message to chat {chat_id}: {e}")
                    games_to_remove.append(chat_id)
        
        # Remove finished games
        for chat_id in games_to_remove:
            del context.bot_data["games"][chat_id]
    
    except Exception as e:
        logger.error(f"Error in timeout handler: {e}")
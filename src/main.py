import os
import sys
import logging
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from src.games.tictactoe_4x4.handlers import (
    start_command, 
    join_command, 
    help_command, 
    button_callback
)
from src.games.tictactoe_4x4.utils import check_game_timeouts
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/telegram_games.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("join", join_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))

    # Add job queue for game timeouts
    job_queue = application.job_queue
    job_queue.run_repeating(check_game_timeouts, interval=5)

    # Start the Bot
    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    main()
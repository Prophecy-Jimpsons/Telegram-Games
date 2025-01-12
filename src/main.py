from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    JobQueue
)

from src.config.settings import BOT_TOKEN, GAME_TIMEOUT_SECONDS
from src.bot.handlers.command_handlers import start, help_command 
from src.bot.handlers.callback_handlers import button_click
from src.bot.handlers.error_handlers import error_handler, timeout_handler
from src.bot.handlers.webapp_handlers import handle_webapp_data
from src.utils.logger import logger

async def init_bot_data(application: Application) -> None:
    """Initialize bot data storage."""
    if "games" not in application.bot_data:
        application.bot_data["games"] = {}
    logger.info("Bot data initialized")

def main() -> None:
    """Start the bot."""
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Initialize bot data
        application.job_queue.run_once(init_bot_data, when=0, data=application)
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command)) 
        
        # Add callback query handler for game board interactions
        application.add_handler(CallbackQueryHandler(button_click))
        
        # Add WebApp data handler
        application.add_handler(MessageHandler(
            filters.StatusUpdate.WEB_APP_DATA,
            handle_webapp_data
        ))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Add job queue for timeout checking
        job_queue = application.job_queue
        job_queue.run_repeating(
            timeout_handler,
            interval=GAME_TIMEOUT_SECONDS,
            first=GAME_TIMEOUT_SECONDS
        )
        
        logger.info("Bot started with automatic timeout checking and WebApp support")
        
        # Start polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
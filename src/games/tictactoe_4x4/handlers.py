from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from .game import TicTacToe4x4
from ...common.theme import GameTheme as theme
import logging
import asyncio

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    try:
        # Check if in private chat
        if update.effective_chat.type == 'private':
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} This game must be played in a group chat!\n"
                "Add me to a group and start playing there! 🎮"
            )
            return

        # Initialize games dict in bot_data if it doesn't exist
        if "games" not in context.bot_data:
            context.bot_data["games"] = {}

        # Check for existing game
        existing_game = context.bot_data["games"].get(chat_id)
        if existing_game and existing_game.phase != "finished":
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} A game is already in progress!\n"
                "Finish the current game or wait for it to time out."
            )
            return

        # Create new game
        game = TicTacToe4x4(chat_id)
        context.bot_data["games"][chat_id] = game
        game.players["X"] = user_id
        game.player_names = {"X": user_name, "O": None}
        game.phase = "waiting"
        game.last_action_time = asyncio.get_event_loop().time()

        # Create welcome message
        welcome_message = (
            f"{theme.format_header(theme.GAME_TITLE)}\n\n"
            f"{theme.STATE['GAME']} New game started!\n\n"
            f"🍌 Player X: {user_name}\n"
            f"🐵 Player O: Waiting...\n\n"
            f"{theme.STATE['WAITING']} Use /join to join the game!\n\n"
            f"Type /help for game rules\n"
            f"{theme.DECORATORS['FOOTER']}"
        )

        # Send initial game message with board
        keyboard = InlineKeyboardMarkup(game.create_keyboard())
        message = await update.message.reply_text(
            welcome_message,
            reply_markup=keyboard
        )
        game.message_id = message.message_id
        logger.info(f"New game started in chat {chat_id} by user {user_id}")

    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            f"{theme.STATE['ERROR']} Failed to start the game. Please try again!"
        )

async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /join command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    try:
        # Check if in private chat
        if update.effective_chat.type == 'private':
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} You can only join games in group chats!"
            )
            return

        # Check if game exists
        game = context.bot_data["games"].get(chat_id)
        if not game:
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} No game in progress!\n"
                "Use /start to create a new game."
            )
            return

        # Check game state
        if game.phase != "waiting":
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} Game already in progress!"
            )
            return

        if game.players.get("O"):
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} Game is already full!"
            )
            return

        if user_id == game.players["X"]:
            await update.message.reply_text(
                f"{theme.STATE['ERROR']} You can't play against yourself! 🙈"
            )
            return

        # Join the game
        game.players["O"] = user_id
        game.player_names["O"] = user_name
        game.phase = "placement"
        game.last_action_time = asyncio.get_event_loop().time()

        # Create game message
        game_message = (
            f"{theme.format_header(theme.GAME_TITLE)}\n\n"
            f"🎮 Game Starting!\n\n"
            f"🍌 Player X: {game.player_names['X']}\n"
            f"🐵 Player O: {game.player_names['O']}\n\n"
            f"{theme.format_turn_message(game.player_names['X'], 'X')}\n"
            f"Placement Phase: Place your pieces (4 each)\n"
            f"{theme.DECORATORS['FOOTER']}"
        )

        # Update game message
        keyboard = InlineKeyboardMarkup(game.create_keyboard())
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=game.message_id,
            text=game_message,
            reply_markup=keyboard
        )
        logger.info(f"Player O ({user_id}) joined the game in chat {chat_id}")

    except Exception as e:
        logger.error(f"Error in join command: {e}")
        await update.message.reply_text(
            f"{theme.STATE['ERROR']} Failed to join the game. Please try again!"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /help command"""
    help_text = (
        f"{theme.format_header('🎮 How to Play')}\n\n"
        "🎯 Game Rules:\n"
        "1. Two players: Player X (🍌) and Player O (🐵)\n"
        "2. Each player gets 4 pieces\n\n"
        "📝 Game Phases:\n"
        "1. Placement Phase:\n"
        "   • Take turns placing pieces\n"
        "   • Each player places 4 pieces\n\n"
        "2. Movement Phase:\n"
        "   • Select your piece to move\n"
        "   • Click empty space to move there\n"
        "   • Click piece again to deselect\n\n"
        "🏆 Win by getting:\n"
        "• Four in a row\n"
        "• Four in a column\n"
        "• Four in a diagonal\n"
        "• Four in a 2x2 square\n\n"
        "⚡ Quick Tips:\n"
        "• Game times out after 60 seconds of inactivity\n"
        "• Use /start to create a new game\n"
        "• Use /join to join an existing game\n"
        f"{theme.DECORATORS['FOOTER']}"
    )
    await update.message.reply_text(help_text)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for game button callbacks"""
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    try:
        # Get current game
        game = context.bot_data["games"].get(chat_id)
        if not game:
            await query.answer(
                f"{theme.STATE['ERROR']} No active game found!", 
                show_alert=True
            )
            return

        # Check game state
        if game.phase == "waiting":
            await query.answer(
                f"{theme.STATE['WAITING']} Waiting for Player O to join!", 
                show_alert=True
            )
            return

        if game.phase == "finished":
            await query.answer(
                "Game is already finished! Start a new game with /start",
                show_alert=True
            )
            return

        # Check if it's player's turn
        if not game.is_player_turn(user_id):
            await query.answer(
                f"{theme.STATE['ERROR']} Not your turn! 🙈", 
                show_alert=True
            )
            return

        # Update last action time
        game.last_action_time = asyncio.get_event_loop().time()

        # Handle the move
        await game.handle_callback(update, context)
        await query.answer()

    except Exception as e:
        logger.error(f"Error in button callback: {e}")
        await query.answer(
            f"{theme.STATE['ERROR']} Something went wrong! Try again.", 
            show_alert=True
        )

def get_handlers():
    """Returns all handlers for the game"""
    return [
        CommandHandler("start", start_command),
        CommandHandler("join", join_command),
        CommandHandler("help", help_command),
        CallbackQueryHandler(button_callback)
    ]
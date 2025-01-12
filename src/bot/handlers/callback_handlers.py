from telegram import Update
from telegram.ext import ContextTypes
from src.games.logic.game_logic import check_winner, find_winning_pattern
from src.games.logic.animations import animate_win
from src.bot.keyboards.game_keyboard import create_keyboard_with_highlight
from src.config.settings import MESSAGES, GAME_TIMEOUT_SECONDS
from src.utils.logger import logger
import asyncio

async def check_inactivity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if the game has timed out due to inactivity.
    Returns True if game was terminated due to timeout.
    """
    chat_id = update.effective_chat.id
    game = context.bot_data["games"].get(chat_id)
    
    if not game or game.phase in ["waiting", "finished"]:
        return False
        
    current_time = asyncio.get_event_loop().time()
    if current_time - game.last_action_time > GAME_TIMEOUT_SECONDS:
        winner = "O" if game.current_player == "X" else "X"
        await context.bot.send_message(
            chat_id=chat_id,
            text=MESSAGES['timeout_win'].format(
                winner=winner,
                winner_name=game.player_names[winner],
                loser=game.current_player
            )
        )
        del context.bot_data["games"][chat_id]
        return True
    return False


def create_game_keyboard(board):
    """Create the game board keyboard"""
    keyboard = []
    for i in range(4):
        row = []
        for j in range(4):
            cell = board[i][j]
            text = cell if cell != " " else "·"
            row.append(InlineKeyboardButton(text, callback_data=f"{i},{j}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all button clicks"""
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    logger.info(f"Received button click from user {user_id} with data: {query.data}")

    try:
        if query.data == "join_game":
            await handle_join_game(update, context)
        else:
            # Handle game moves
            await handle_game_move(update, context)

    except Exception as e:
        logger.error(f"Error in button_click: {e}")
        await query.answer("Error processing your request!")

async def handle_join_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle join game button click"""
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    logger.info(f"User {user_id} attempting to join game in chat {chat_id}")

    try:
        game = context.bot_data["games"].get(chat_id)
        if not game:
            await query.answer("No active game found!")
            return

        if game.phase != "waiting":
            await query.answer("Game already in progress!")
            return

        if user_id == game.players["X"]:
            await query.answer("You can't play against yourself!")
            return

        if game.players["O"]:
            await query.answer("Game is full!")
            return

        # Join as player O
        game.players["O"] = user_id
        game.player_names["O"] = user_name
        game.phase = "placement"

        # Create the keyboard using your existing function
        keyboard = create_keyboard_with_highlight(game.board)

        # Update the message
        await query.edit_message_text(
            f"Game started!\n"
            f"Player X: {game.player_names['X']}\n"
            f"Player O: {game.player_names['O']}\n"
            f"Player X's turn (Placement phase: {game.pieces['X']}/4 pieces placed)",
            reply_markup=keyboard
        )

        await query.answer("Successfully joined the game!")
        logger.info(f"Player {user_name} ({user_id}) successfully joined the game")

    except Exception as e:
        logger.error(f"Error in handle_join_game: {e}")
        await query.answer("Error joining the game!")

async def handle_game_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle game move button clicks"""
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    try:
        game = context.bot_data["games"].get(chat_id)
        if not game:
            await query.answer("No active game found!")
            return

        if game.phase == "waiting":
            await query.answer("Waiting for players to join!")
            return

        if user_id != game.players[game.current_player]:
            await query.answer("Not your turn!")
            return

        # Get row and column from callback data
        row, col = map(int, query.data.split(","))

        # Handle placement phase
        if game.phase == "placement":
            if game.board[row][col] != " ":
                await query.answer("Space already occupied!")
                return

            # Place piece
            game.board[row][col] = game.current_player
            game.pieces[game.current_player] += 1

            # Update keyboard
            keyboard = create_keyboard_with_highlight(game.board)

            # Switch player
            next_player = "O" if game.current_player == "X" else "X"
            game.current_player = next_player

            # Update message
            await query.edit_message_text(
                f"Player {next_player}'s turn\n"
                f"Placement phase: {game.pieces[next_player]}/4 pieces placed",
                reply_markup=keyboard
            )

        await query.answer()

    except Exception as e:
        logger.error(f"Error in handle_game_move: {e}")
        await query.answer("Error processing move!")
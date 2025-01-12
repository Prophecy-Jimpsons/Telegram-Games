# src/bot/handlers/webapp_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.logger import logger
from src.games.models.game_state import GameState
from src.games.logic.game_logic import check_winner, find_winning_pattern
import json

async def send_game_update(context: ContextTypes.DEFAULT_TYPE, chat_id: int, game: GameState) -> None:
    """Send game state update to all players"""
    game_state = game.to_dict()
    
    # Send update to both players
    for player_symbol in ["X", "O"]:
        player_id = game.players[player_symbol]
        if player_id:
            try:
                await context.bot.send_message(
                    chat_id=player_id,
                    text=json.dumps({
                        "type": "gameUpdate",
                        "state": game_state
                    })
                )
            except Exception as e:
                logger.error(f"Error sending update to player {player_id}: {e}")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle data received from the WebApp"""
    try:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        # Parse the data received from WebApp
        try:
            data = json.loads(update.effective_message.web_app_data.data)
            logger.info(f"Received WebApp data: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data received: {e}")
            return

        # Get or create game state
        if "games" not in context.bot_data:
            context.bot_data["games"] = {}
        
        game = context.bot_data["games"].get(chat_id)
        if not game:
            game = GameState(chat_id)
            context.bot_data["games"][chat_id] = game
            game.players["X"] = user_id
            game.player_names["X"] = user_name

        # Handle different game actions
        action = data.get("action")
        
        if action == "join":
            if game.players["O"] is None and user_id != game.players["X"]:
                game.players["O"] = user_id
                game.player_names["O"] = user_name
                game.phase = "placement"
                await update.effective_message.reply_text(
                    f"Player {user_name} joined as O!"
                )
                # Send initial game state to both players
                await send_game_update(context, chat_id, game)
            
        elif action == "move":
            if user_id != game.players[game.current_player]:
                logger.warning(f"Invalid move attempt by user {user_id}")
                return

            success = game.handle_webapp_move(
                user_id=user_id,
                position=data.get("position"),
                selected=data.get("selected")
            )
            
            if success:
                # Check for winner
                winner = check_winner(game.board)
                if winner:
                    game.phase = "finished"
                    winning_pattern = find_winning_pattern(game.board)
                    await send_game_update(context, chat_id, game)
                    await update.effective_message.reply_text(
                        f"🎉 Player {game.current_player} ({game.player_names[game.current_player]}) wins!"
                    )
                    del context.bot_data["games"][chat_id]
                    return

                # Update game phase if needed
                if game.phase == "placement" and all(v == 4 for v in game.pieces.values()):
                    game.phase = "movement"
                    game.current_player = "X"
                else:
                    game.current_player = "O" if game.current_player == "X" else "X"

                # Send update to all players
                await send_game_update(context, chat_id, game)

        game.update_last_action_time()
        logger.info(f"Game action {action} processed successfully")

    except Exception as e:
        logger.error(f"Error handling WebApp data: {e}")
        await update.effective_message.reply_text(
            "Sorry, there was an error processing your move. Please try again."
        )
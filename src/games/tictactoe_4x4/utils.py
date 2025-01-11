import asyncio
from typing import Dict, Any
from telegram.ext import ContextTypes
from ...common.theme import GameTheme as theme

async def check_game_timeouts(context: ContextTypes.DEFAULT_TYPE):
    """Check for game timeouts and handle them"""
    games_to_remove = []
    current_time = asyncio.get_event_loop().time()
    
    for chat_id, game in context.bot_data.get("games", {}).items():
        if game.phase not in ["finished", "waiting"]:
            if current_time - game.last_action_time > 60:  # 60 seconds timeout
                winner = "O" if game.current_player == "X" else "X"
                winner_name = game.player_names[winner]
                
                timeout_message = (
                    f"{theme.STATE['TIMEOUT']}\n\n"
                    f"Player {theme.SYMBOLS[winner]} {winner_name} wins by default!\n"
                    f"Player {theme.SYMBOLS[game.current_player]} was inactive too long.\n\n"
                    f"Use /start to begin a new game! 🎮"
                )
                
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=timeout_message
                )
                games_to_remove.append(chat_id)
    
    # Clean up timed out games
    for chat_id in games_to_remove:
        del context.bot_data["games"][chat_id]

def format_game_stats(game_data: Dict[str, Any]) -> str:
    """Format game statistics for display"""
    return (
        f"{theme.format_header('Game Stats')}\n"
        f"Total Moves: {game_data['moves']}\n"
        f"Game Duration: {game_data['duration']}s\n"
        f"Winner: {theme.SYMBOLS[game_data['winner']]} "
        f"({game_data['winner_name']})\n"
        f"{theme.DECORATORS['FOOTER']}"
    )
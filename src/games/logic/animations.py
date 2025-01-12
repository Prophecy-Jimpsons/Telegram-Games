import asyncio
from typing import List, Tuple
from telegram import Bot
from telegram.error import TelegramError
from ...bot.keyboards.game_keyboard import create_keyboard_with_highlight
from ..models.game_state import GameState

async def animate_win(
    bot: Bot,
    game: GameState,
    winner: str,
    pattern: List[Tuple[int, int]]
) -> None:
    """
    Animate the winning move with emojis.
    
    Args:
        bot: Telegram bot instance
        game: Current game state
        winner: The winning player ("X" or "O")
        pattern: List of winning positions
    """
    animations = ["🎮", "🎲", "🎯", "🎪", "🎨"]
    
    try:
        for anim in animations:
            keyboard = create_keyboard_with_highlight(game.board, winning_pattern=pattern)
            await bot.edit_message_text(
                chat_id=game.chat_id,
                message_id=game.message_id,
                text=f"{anim} WINNER! {anim}\n\n"
                     f"Player {winner} ({game.player_names[winner]}) wins!\n"
                     f"Final Board Position:",
                reply_markup=keyboard
            )
            await asyncio.sleep(0.5)
    except TelegramError as e:
        # Log error but don't raise - animation failure shouldn't break the game
        print(f"Animation error: {e}")
        # Still show final state
        keyboard = create_keyboard_with_highlight(game.board, winning_pattern=pattern)
        try:
            await bot.edit_message_text(
                chat_id=game.chat_id,
                message_id=game.message_id,
                text=f"🏆 WINNER! 🏆\n\n"
                     f"Player {winner} ({game.player_names[winner]}) wins!\n"
                     f"Final Board Position:",
                reply_markup=keyboard
            )
        except TelegramError:
            pass  # Ignore if final update fails too
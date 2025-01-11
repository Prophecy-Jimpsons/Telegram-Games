from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from telegram import Update, Message
from telegram.ext import ContextTypes

class BaseGame(ABC):
    def __init__(self, chat_id: int):
        self.chat_id: int = chat_id
        self.message_id: Optional[int] = None
        self.players: Dict[str, Any] = {}
        self.current_player: Optional[str] = None
        self.phase: str = "waiting"
        self.last_action_time: float = 0

    @abstractmethod
    async def initialize_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Message:
        """Initialize the game state and send the first message"""
        pass

    @abstractmethod
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from the game's inline keyboard"""
        pass

    @abstractmethod
    def get_game_state_message(self) -> str:
        """Get the current game state as a formatted message"""
        pass

    @abstractmethod
    def create_keyboard(self) -> list:
        """Create the game's inline keyboard"""
        pass

    @property
    @abstractmethod
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        pass

    def is_player_turn(self, user_id: int) -> bool:
        """Check if it's the given user's turn"""
        if not self.current_player or user_id not in self.players.values():
            return False
        return self.players[self.current_player] == user_id
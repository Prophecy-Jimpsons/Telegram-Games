from typing import Dict, Optional, List, Tuple
import asyncio

class GameState:
    """
    Represents the state of a 4x4 Tic-Tac-Toe game.
    Handles game state management and validation.
    """
    def __init__(self, chat_id: int = None):  # Make chat_id optional with default None
        self.chat_id: int = chat_id
        self.board: List[List[str]] = [[" " for _ in range(4)] for _ in range(4)]
        self.current_player: str = "X"
        self.pieces: Dict[str, int] = {"X": 0, "O": 0}
        self.players: Dict[str, Optional[int]] = {"X": None, "O": None}
        self.player_names: Dict[str, Optional[str]] = {"X": None, "O": None}
        self.phase: str = "waiting"  # waiting, placement, movement, finished
        self.selected_piece: Optional[Tuple[int, int]] = None
        self.message_id: Optional[int] = None
        self.last_action_time = asyncio.get_event_loop().time()

    def to_dict(self) -> dict:
        """Convert game state to dictionary for WebApp"""
        return {
            "board": self.board,
            "currentPlayer": self.current_player,
            "phase": self.phase,
            "piecesPlaced": self.pieces,
            "players": {
                "X": {"id": self.players["X"], "name": self.player_names["X"]},
                "O": {"id": self.players["O"], "name": self.player_names["O"]}
            }
        }

    def update_last_action_time(self) -> None:
        """Update the last action time to prevent timeout"""
        self.last_action_time = asyncio.get_event_loop().time()

    def handle_webapp_move(self, user_id: int, position: int, selected: Optional[int] = None) -> bool:
        """Handle move from WebApp"""
        if user_id != self.players[self.current_player]:
            return False
            
        row, col = position // 4, position % 4
        
        if self.phase == "placement":
            if self.board[row][col] != " ":
                return False
                
            self.board[row][col] = self.current_player
            self.pieces[self.current_player] += 1
            return True
            
        elif self.phase == "movement" and selected is not None:
            old_row, old_col = selected // 4, selected % 4
            if self.board[old_row][old_col] != self.current_player:
                return False
                
            if self.board[row][col] != " ":
                return False
                
            self.board[old_row][old_col] = " "
            self.board[row][col] = self.current_player
            return True
            
        return False

    # Might need to remove below code 
    def _handle_placement(self, position: int) -> bool:
        row, col = position // 4, position % 4
        if self.board[row][col] != " ":
            return False
            
        self.board[row][col] = self.current_player
        self.pieces[self.current_player] += 1
        return True

    def _handle_movement(self, position: int, selected: Optional[int]) -> bool:
        if selected is None:
            return False
            
        old_row, old_col = selected // 4, selected % 4
        new_row, new_col = position // 4, position % 4
        
        if self.board[old_row][old_col] != self.current_player:
            return False
            
        if self.board[new_row][new_col] != " ":
            return False
            
        self.board[old_row][old_col] = " "
        self.board[new_row][new_col] = self.current_player
        return True
from typing import List, Tuple, Optional
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...common.base_game import BaseGame
from ...common.theme import GameTheme as theme

class TicTacToe4x4(BaseGame):
    def __init__(self, chat_id: int):
        super().__init__(chat_id)
        self.board = [[" " for _ in range(4)] for _ in range(4)]
        self.pieces = {"X": 0, "O": 0}
        self.current_player = "X"
        self.selected_piece: Optional[Tuple[int, int]] = None
        self.winner = None
        self.winning_pattern = None

    def create_keyboard(self) -> List[List[InlineKeyboardButton]]:
        keyboard = []
        for i, row in enumerate(self.board):
            keyboard_row = []
            for j, cell in enumerate(row):
                button_text = self._get_cell_display(i, j)
                keyboard_row.append(
                    InlineKeyboardButton(button_text, callback_data=f"{i},{j}")
                )
            keyboard.append(keyboard_row)
        return keyboard

    def _get_cell_display(self, i: int, j: int) -> str:
        cell = self.board[i][j]
        
        # Empty cell
        if cell == " ":
            return theme.SYMBOLS["EMPTY"]
        
        # Selected piece
        if self.selected_piece and (i, j) == self.selected_piece:
            return f"{theme.SYMBOLS['SELECTED']}{theme.SYMBOLS[cell]}"
            
        # Winning piece
        if self.winning_pattern and (i, j) in self.winning_pattern:
            return f"{theme.SYMBOLS['WINNER']}{theme.SYMBOLS[cell]}"
            
        # Normal piece
        return theme.SYMBOLS[cell]

    def get_game_state_message(self) -> str:
        if self.phase == "waiting":
            return theme.MESSAGES["WAITING"]

        if self.winner:
            return theme.MESSAGES["WINNER"].format(
                symbol=theme.SYMBOLS[self.winner],
                player_name=self.player_names[self.winner]
            )

        phase_display = "Placement" if self.phase == "placement" else "Movement"
        pieces_info = f"Pieces placed: {self.pieces[self.current_player]}/4" \
            if self.phase == "placement" else ""

        return (
            f"{theme.format_header(theme.GAME_TITLE)}\n"
            f"{theme.format_turn_message(self.player_names[self.current_player], self.current_player)}\n"
            f"Phase: {phase_display}\n"
            f"{pieces_info}\n"
            f"{theme.DECORATORS['SEPARATOR']}"
        )

    def check_winner(self) -> Optional[str]:
        # Check rows and columns
        for i in range(4):
            if all(self.board[i][j] == "X" for j in range(4)) or \
               all(self.board[j][i] == "X" for j in range(4)):
                return "X"
            if all(self.board[i][j] == "O" for j in range(4)) or \
               all(self.board[j][i] == "O" for j in range(4)):
                return "O"

        # Check diagonals
        if all(self.board[i][i] == "X" for i in range(4)) or \
           all(self.board[i][3-i] == "X" for i in range(4)):
            return "X"
        if all(self.board[i][i] == "O" for i in range(4)) or \
           all(self.board[i][3-i] == "O" for i in range(4)):
            return "O"

        # Check 2x2 squares
        for i in range(3):
            for j in range(3):
                if all(self.board[i+di][j+dj] == "X" 
                      for di, dj in [(0,0), (0,1), (1,0), (1,1)]):
                    return "X"
                if all(self.board[i+di][j+dj] == "O"
                      for di, dj in [(0,0), (0,1), (1,0), (1,1)]):
                    return "O"

        return None

    def find_winning_pattern(self) -> List[Tuple[int, int]]:
        # Similar to check_winner but returns the winning positions
        # Implementation details here...
        pass

    @property
    def is_game_over(self) -> bool:
        return self.winner is not None or self.phase == "finished"

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        row, col = map(int, query.data.split(","))

        if self.phase == "placement":
            await self._handle_placement_phase(row, col, update, context)
        elif self.phase == "movement":
            await self._handle_movement_phase(row, col, update, context)

        # Update game message
        keyboard = InlineKeyboardMarkup(self.create_keyboard())
        await query.edit_message_text(
            text=self.get_game_state_message(),
            reply_markup=keyboard
        )

    async def _handle_placement_phase(self, row: int, col: int, 
                                    update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.board[row][col] != " ":
            await update.callback_query.answer("Space already occupied! 🙈")
            return

        self.board[row][col] = self.current_player
        self.pieces[self.current_player] += 1

        # Check if placement phase is complete
        if self.pieces["X"] == 4 and self.pieces["O"] == 4:
            self.phase = "movement"
            self.current_player = "X"
            return

        self.current_player = "O" if self.current_player == "X" else "X"

    async def _handle_movement_phase(self, row: int, col: int,
                                   update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.selected_piece:
            if self.board[row][col] != self.current_player:
                await update.callback_query.answer(
                    "Select your own piece! 🐒", show_alert=True
                )
                return
            self.selected_piece = (row, col)
            return

        if (row, col) == self.selected_piece:
            self.selected_piece = None
            await update.callback_query.answer("Piece deselected 🔄")
            return

        if self.board[row][col] != " ":
            await update.callback_query.answer(
                "That space is occupied! 🙈", show_alert=True
            )
            return

        # Move the piece
        old_row, old_col = self.selected_piece
        self.board[row][col] = self.current_player
        self.board[old_row][old_col] = " "
        self.selected_piece = None

        # Check for winner
        winner = self.check_winner()
        if winner:
            self.winner = winner
            self.winning_pattern = self.find_winning_pattern()
            self.phase = "finished"
            await self._animate_win(update, context)
            return

        self.current_player = "O" if self.current_player == "X" else "X"

    async def _animate_win(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        animations = ["🎉", "🌟", "🎊", "✨", "👑"]
        query = update.callback_query
        
        for anim in animations:
            keyboard = InlineKeyboardMarkup(self.create_keyboard())
            await query.edit_message_text(
                f"{anim} WINNER! {anim}\n"
                f"Player {self.winner} ({self.player_names[self.winner]}) wins!\n"
                f"{theme.MESSAGES['WINNER'].format(symbol=theme.SYMBOLS[self.winner], player_name=self.player_names[self.winner])}",
                reply_markup=keyboard
            )
            await asyncio.sleep(0.5)
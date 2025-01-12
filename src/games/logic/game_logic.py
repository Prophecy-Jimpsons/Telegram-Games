from typing import List, Optional, Tuple

def find_winning_pattern(board: List[List[str]]) -> Optional[List[Tuple[int, int]]]:
    """
    Find a winning pattern on the board.
    Returns the list of winning positions or None if no winner.
    """
    # Check rows and columns
    for i in range(4):
        if all(board[i][j] == "X" for j in range(4)):
            return [(i, j) for j in range(4)]
        if all(board[i][j] == "O" for j in range(4)):
            return [(i, j) for j in range(4)]
        if all(board[j][i] == "X" for j in range(4)):
            return [(j, i) for j in range(4)]
        if all(board[j][i] == "O" for j in range(4)):
            return [(j, i) for j in range(4)]

    # Check diagonals
    if all(board[i][i] == "X" for i in range(4)):
        return [(i, i) for i in range(4)]
    if all(board[i][i] == "O" for i in range(4)):
        return [(i, i) for i in range(4)]
    if all(board[i][3-i] == "X" for i in range(4)):
        return [(i, 3-i) for i in range(4)]
    if all(board[i][3-i] == "O" for i in range(4)):
        return [(i, 3-i) for i in range(4)]

    # Check 2x2 squares
    for i in range(3):
        for j in range(3):
            if all(board[i+di][j+dj] == "X" for di, dj in [(0,0), (0,1), (1,0), (1,1)]):
                return [(i+di, j+dj) for di, dj in [(0,0), (0,1), (1,0), (1,1)]]
            if all(board[i+di][j+dj] == "O" for di, dj in [(0,0), (0,1), (1,0), (1,1)]):
                return [(i+di, j+dj) for di, dj in [(0,0), (0,1), (1,0), (1,1)]]

    return None

def check_winner(board: List[List[str]]) -> Optional[str]:
    """
    Check if there's a winner on the board.
    Returns the winning player ("X" or "O") or None if no winner.
    """
    pattern = find_winning_pattern(board)
    if pattern:
        return board[pattern[0][0]][pattern[0][1]]
    return None

def is_board_full(board: List[List[str]]) -> bool:
    """Check if the board is completely filled."""
    return all(cell != " " for row in board for cell in row)

def get_valid_moves(board: List[List[str]]) -> List[Tuple[int, int]]:
    """Get all valid moves (empty spaces) on the board."""
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] == " "]
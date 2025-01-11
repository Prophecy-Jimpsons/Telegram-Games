class GameTheme:
    # Brand Colors (Used in emoji selections and text formatting)
    PRIMARY_COLOR = "#fcaf05"    # Banana Yellow
    SECONDARY_COLOR = "#0568fc"  # Bright Blue

    # Game Title
    GAME_TITLE = "🐒 Monkey TicTacToe 🍌"
    
    # Player Symbols
    SYMBOLS = {
        "X": "🍌",  # Banana for Player X
        "O": "🐵",  # Monkey face for Player O
        "EMPTY": "🌴",  # Palm tree for empty spaces
        "SELECTED": "✨",  # Sparkles for selected piece
        "WINNER": "👑",  # Crown for winning pieces
    }

    # Game State Emojis
    STATE = {
        "WAITING": "🎪",
        "PLAYING": "🎮",
        "FINISHED": "🏆",
        "ERROR": "🙈",
        "TIMEOUT": "⏰",
    }

    # Message Decorators
    DECORATORS = {
        "HEADER": "🎪 ═══════════════ 🎪",
        "FOOTER": "🌴 ═══════════════ 🌴",
        "TURN_INDICATOR": "👉",
        "SEPARATOR": "•═•═•═•═•═•═•═•═•",
    }

    # Button Styles (Used in message formatting)
    BUTTON_STYLES = {
        "NORMAL": "⬜",
        "HIGHLIGHT": "🟡",
        "SELECTED": "🔵",
        "WINNER": "🌟",
    }

    # Message Templates
    MESSAGES = {
        "WELCOME": (
            "{header}\n"
            "Welcome to {game_title}!\n"
            "Swing from tree to tree to win! 🌴\n"
            "{footer}"
        ),
        "WAITING": (
            "🐒 Waiting for another player to join!\n"
            "Use /join to join the game!"
        ),
        "TURN": (
            "{symbol} It's {player_name}'s turn!\n"
            "Place your {piece} wisely!"
        ),
        "WINNER": (
            "🎉 WINNER! 🎉\n"
            "{symbol} {player_name} wins the game!\n"
            "🍌 Bananas for everyone! 🍌"
        ),
        "TIMEOUT": (
            "⏰ Time's up!\n"
            "The monkeys got tired of waiting...\n"
            "Game Over!"
        ),
    }

    @classmethod
    def format_board(cls, board: list) -> str:
        """Format the game board with themed elements"""
        return f"{cls.DECORATORS['HEADER']}\n" + \
               "\n".join([" ".join(row) for row in board]) + \
               f"\n{cls.DECORATORS['FOOTER']}"

    @classmethod
    def format_turn_message(cls, player_name: str, symbol: str) -> str:
        """Format the turn message with themed elements"""
        piece = cls.SYMBOLS[symbol]
        return cls.MESSAGES["TURN"].format(
            symbol=cls.DECORATORS["TURN_INDICATOR"],
            player_name=player_name,
            piece=piece
        )

    @classmethod
    def format_header(cls, title: str) -> str:
        """Format a header with themed elements"""
        return f"{cls.DECORATORS['HEADER']}\n{title}\n{cls.DECORATORS['SEPARATOR']}"
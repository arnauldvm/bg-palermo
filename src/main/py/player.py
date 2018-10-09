from typing import List, Dict

from deck import Card


class Player:

    def __init__(self, color: str, board, cash: int, due: int, hand: Dict[str, List[Card]]):
        self.color = color
        self.board = board
        self.cash = cash
        self.due = due
        self.hand = hand

    def __repr__(self):
        return ("Player("
                f"color:{self.color!r},\n"
                f"board:{self.board!r},\n"
                f"cash:{self.cash!r}, due:{self.due!r},\n"
                f"hand:{self.hand!r}"
                ")")

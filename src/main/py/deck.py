from typing import List, Dict, NewType
from collections import namedtuple

import random

Card = NewType('Card', namedtuple)


class Pile(list):  # list of Card?
    def __init__(self, *args):
        list.__init__(self, *args)

    def __str__(self):
        return f"{ len(self) } cards"

    def shuffle(self) -> None:
        random.shuffle(self)

    def draw(self) -> Card:
        return self.pop(0)

    # def draw_n(self, n_cards: int) -> Pile:
    #     return Pile([self.draw() for _ in range(n_cards)])
    #
    # ! Not possible to reference Pile when not yet defined
    # Solved by: from __future__ import annotations
    # ... but this is not supported by Python before 3.6
    # => Use the workaround here below


def _Pile_draw_n(pile: Pile, n_cards: int) -> Pile:
    return Pile([pile.draw() for _ in range(n_cards)])


setattr(Pile, 'draw_n', _Pile_draw_n)


class DeckSystem:

    def __init__(self, deck: Pile):
        self.deck = deck
        self.river = Pile([])
        self.discard = Pile([])

    def reset_deck(self) -> None:
        self.deck.extend(self.discard)
        self.discard.clear()
        self.deck.shuffle()

    def discard_pile(self, cards: Pile) -> None:
        self.discard.extend(cards)

    def feed_river(self, n_cards) -> None:
        self.river = self.deck.draw_n(n_cards)

    def __str__(self):
        return (
            f"{ self.deck } in deck + "
            f"{ self.river } in river + "
            f"{ self.discard } in discard pile"
        )

    def draw_and_choose(self, n_draw: int, n_choose: int) -> Pile:
        draw = self.deck.draw_n(n_draw)
        # IA rule: random choice (should be externalized to an IA claas)
        draw.shuffle()
        chosen = draw.draw_n(n_choose)
        self.discard_pile(draw)
        return chosen

    def __repr__(self):
        return ("DeckSystem(\n"
                f"deck:{self.deck!r},\n"
                f"river:{self.river!r},\n"
                f"discard:{self.discard!r}\n"
                ")")

from __future__ import annotations  # required for being able to declare a method returing type of its class

from typing import List, Dict, NewType
from collections import namedtuple

import random

Card = NewType('Card', namedtuple)


class Pile(list):  # list of Card?
    def __init__(self, *args):
        list.__init__(self, *args)

    def shuffle(self) -> None:
        random.shuffle(self)

    def draw(self) -> Card:
        return self.pop(0)

    def draw_n(self, n_cards: int) -> Pile:
        return Pile([self.draw() for _ in range(n_cards)])


class DeckSystem:

    def __init__(self, deck: Pile):
        self.deck = deck
        self.river = Pile([])
        self.discard = Pile([])

    def reset_deck(self) -> None:
        self.deck.extend(self.discard)
        self.discard.clear()
        self.deck.shuffle()

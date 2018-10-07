from typing import List, Dict, NewType
from collections import namedtuple

Card = NewType('Card', namedtuple)


class Pile(list):  # list of Card?
    def __init__(self, *args):
        list.__init__(self, *args)


class DeckSystem:

    def __init__(self, deck: Pile):
        self.deck = deck
        self.river = Pile([])
        self.discard = Pile([])

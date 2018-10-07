from typing import List, Dict, NewType
from collections import namedtuple

Card = NewType('Card', namedtuple)
Pile = NewType('Pile', List[Card])  # A deck is a list of named tuples

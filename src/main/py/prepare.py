#!/usr/bin/env python3

from typing import List, Dict, Any, NewType
from collections import namedtuple
import random

from load_data import resources, contracts, facilities, trade, colors
from deck import Card, Pile, DeckSystem


def prepare_deck(df) -> Pile:
    deck = Pile(
        [
            item
            for df_noindex in [df.assign(kind=df.index).reset_index(drop=True)]
            for item in df_noindex.itertuples()
            for _ in range(item.count)
            # for _, item in df_noindex.iterrows()
            # for _ in range(item['count'])
        ]
    )

    # deck = [ deck[i] for l in [len(deck)] for i in random.sample(range(l), l) ]
    deck.shuffle()
    assert len(deck) == df['count'].sum(), f'Not enough cards in prepared deck: {len(deck)}'
    assert deck[0].Index != deck[1].Index, 'Deck not shuffled'
    return deck


contracts = DeckSystem(prepare_deck(contracts))
facilities = DeckSystem(prepare_deck(facilities))

# plateau central
# * cours des matières recyclées
# * "tarifs" de la Mafia,
# * piste de dette à la Mafia


def discard(discard_pile: Pile, cards: Pile) -> None:
    discard_pile.extend(cards)


def draw_and_choose(deckSys: DeckSystem, n_draw: int, n_choose: int) -> Pile:
    draw = deckSys.deck.draw_n(n_draw)
    # IA rule: random choice (should be externalized to an IA claas)
    draw.shuffle()
    chosen = draw.draw_n(n_choose)
    discard(deckSys.discard, draw)
    return chosen


def prepare_player(color):
    global contracts
    global facilities
    board = {}
    # * plateau individuel
    #   - livraison vrac
    #   - livraison trié
    #   - stockage
    #   - décontamination
    #   - incinération
    #   - recyclage
    # * tirage initial de cartes:
    player_contracts = draw_and_choose(contracts, 3, 1)
    #   Should externalize '3' and '1' as rule parameters
    player_facilities = draw_and_choose(facilities, 6, 3)
    #   Should externalize '6' and '3' as rule parameters
    return {'color': color, 'board': board, 'cash': 20, 'due': 0,
            'hand': {'contracts': player_contracts, 'facilities': player_facilities}}


def prepare_players(n_players: int) -> Dict[str, Any]:
    first_player = random.randrange(n_players)
    random_colors = [_.color for _ in colors.itertuples()]
    random.shuffle(random_colors)
    players = [prepare_player(random_colors[num]) for num in range(n_players)]
    return {'first': first_player, 'list': players}


def prepare_river(deckSys: DeckSystem, n_cards: int) -> None:
    deckSys.reset_deck()
    river = deckSys.deck.draw_n(n_cards)
    deckSys.river = river


def prepare_rivers(n_players: int):
    global contracts
    global facilities
    prepare_river(contracts, n_players)
    #   Should externalize n_players as a rule parameter
    prepare_river(facilities, 3)
    #   Should externalize '3' as a rule parameter


# TODO: create 'Pile' class with methods: shuffle, draw...
# TODO: create class for the system: deck Pile + discard Pile + river Pile

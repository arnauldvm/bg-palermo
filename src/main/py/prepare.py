#!/usr/bin/env python3

from typing import List, Tuple, Dict, Any, NewType

from load_data import resources, contracts, facilities, trade, colors

import random

Deck = NewType('Deck', List[Tuple])  # A deck is a list of tuples


def prepare_deck(df) -> Deck:
    deck = Deck(
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
    random.shuffle(deck)
    assert len(deck) == df['count'].sum(), f'Not enough cards in prepared deck: {len(deck)}'
    assert deck[0].Index != deck[1].Index, 'Deck not shuffled'
    return deck


contracts_deck = prepare_deck(contracts)
facilities_deck = prepare_deck(facilities)

# plateau central
# * cours des matières recyclées
# * "tarifs" de la Mafia,
# * piste de dette à la Mafia


def draw(deck: Deck) -> Tuple:
    return deck.pop(0)


def draw_n(deck: Deck, n_cards: int) -> Deck:
    return Deck([draw(deck) for _ in range(n_cards)])


contracts_discard = Deck([])
facilities_discard = Deck([])


def discard(discard_pile: Deck, cards: Deck) -> None:
    discard_pile.extend(cards)


def draw_and_choose(deck: Deck, discard_pile: Deck, n_draw: int, n_choose: int) -> Deck:
    draw = draw_n(deck, n_draw)
    # IA rule: random choice (should be externalized to an IA claas)
    random.shuffle(draw)
    chosen = draw_n(draw, n_choose)
    discard(discard_pile, draw)
    return chosen


def prepare_player(color):
    global contracts_deck
    global facilities_deck
    global contracts_discard
    global facilities_discard
    board = {}
    # * plateau individuel
    #   - livraison vrac
    #   - livraison trié
    #   - stockage
    #   - décontamination
    #   - incinération
    #   - recyclage
    # * tirage initial de cartes:
    player_contracts = draw_and_choose(contracts_deck, contracts_discard, 3, 1)
    #   Should externalize '3' and '1' as rule parameters
    player_facilities = draw_and_choose(facilities_deck, facilities_discard, 6, 3)
    #   Should externalize '6' and '3' as rule parameters
    return {'color': color, 'board': board, 'cash': 20, 'due': 0,
            'hand': {'contracts': player_contracts, 'facilities': player_facilities}}


def prepare_players(n_players: int) -> Dict[str, Any]:
    first_player = random.randrange(n_players)
    random_colors = [_.color for _ in colors.itertuples()]
    random.shuffle(random_colors)
    players = [prepare_player(random_colors[num]) for num in range(n_players)]
    return {'first': first_player, 'list': players}


def reset_deck(deck: Deck, discard: Deck) -> None:
    deck.extend(discard)
    discard.clear()
    random.shuffle(deck)


def prepare_river(deck: Deck, discard: Deck, n_cards: int) -> Deck:
    reset_deck(deck, discard)
    river = draw_n(deck, n_cards)
    return river


contracts_river = Deck([])
facilities_river = Deck([])


def prepare_rivers(n_players: int):
    global contracts_deck
    global facilities_deck
    global contracts_river
    global facilities_river
    contracts_river = prepare_river(contracts_deck, contracts_discard, n_players)
    #   Should externalize n_players as a rule parameter
    facilities_river = prepare_river(facilities_deck, facilities_discard, 3)
    #   Should externalize '3' as a rule parameter

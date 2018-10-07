#!/usr/bin/env python3

from typing import List, Tuple, NewType

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


def prepare_player(color):
    board = {}
    # * plateau individuel
    #   - livraison vrac
    #   - livraison trié
    #   - stockage
    #   - décontamination
    #   - incinération
    #   - recyclage
    # * tirage initial de cartes:
    #   - contrat (choix de 1 parmi 3)
    #   - équipements (choix de 3 parmi 6)
    return {'color': color, 'board': board, 'cash': 20, 'due': 0}


def prepare_players(n_players: int):
    first_player = random.randrange(n_players)
    random_colors = [_.color for _ in colors.itertuples()]
    random.shuffle(random_colors)
    players = [prepare_player(random_colors[num]) for num in range(n_players)]
    return {'first': first_player, 'list': players}

# disposer  les decks et "rivières" :
# * remélanger toutes les cartes restantes, révéler n contrats
# * remélanger toutes les cartes restantes, révéler 3 équipements

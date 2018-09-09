#!/usr/bin/env python3

from load_data import resources, contracts, facilities, trade

import random

def prepare_deck(df):
    deck = [ item
              for df_noindex in [df.assign(kind=df.index).reset_index(drop = True)]
              for item in df_noindex.itertuples()
              for _ in range(item.count)
              # for _, item in df_noindex.iterrows()
              # for _ in range(item['count'])
          ]

    # deck = [ deck[i] for l in [len(deck)] for i in random.sample(range(l), l) ]
    random.shuffle(deck)
    assert len(deck)==df['count'].sum(), f'Not enough cards in prepared deck: {len(deck)}'
    assert deck[0].Index!=deck[1].Index, 'Deck not shuffled'
    return deck

contracts_deck = prepare_deck(contracts)
facilities_deck = prepare_deck(facilities)

# plateau central
# * cours des matières recyclées
# * "tarifs" de la Mafia,
# * piste de dette à la Mafia

# assigner pion premier joueur

# par joueur :
# * choisir une couleur
# * plateau individuel
#   - livraison vrac
#   - livraison trié
#   - stockage
#   - décontamination
#   - incinération
#   - recyclage
# * compte individuel (init: 20 (Mβ))
# * initialiser marqueur de dette à 0 (Mβ) (sur le plateau central dans le jeu physique)
# * tirage initial de cartes:
#   - contrat (choix de 1 parmi 3)
#   - équipements (choix de 3 parmi 6)

# disposer  les decks et "rivières" :
# * remélanger toutes les cartes restantes, révéler n contrats
# * remélanger toutes les cartes restantes, révéler 3 équipements

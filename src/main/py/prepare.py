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
    return deck

contracts_deck = prepare_deck(contracts)
facilities_deck = prepare_deck(facilities)

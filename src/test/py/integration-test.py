#!/usr/bin/env python3

from prepare import prepare_players
from prepare import contracts
from prepare import facilities
from prepare import prepare_rivers

players = prepare_players(4)
print(f'contracts { contracts.short_description() }')
print(f'facilities { facilities.short_description() }')

prepare_rivers(4)
print(f'contracts { contracts.short_description() }')
print(f'facilities { facilities.short_description() }')

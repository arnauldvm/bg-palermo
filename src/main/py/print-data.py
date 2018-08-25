#!/usr/bin/env python3

from load_data import resources, contracts, facilities, trade

def print_data(name, dataframe):
	print(f'\n{name}:\n{dataframe}')

print_data('Resources', resources)
print_data('Contracts', contracts)
print_data('Facilities', facilities)
print_data('Trade', trade)

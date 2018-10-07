#!/usr/bin/env python3

import pandas as pd

from load_data import resources, contracts, facilities, trade


def print_data(name: str, dataframe: pd.DataFrame) -> None:
    print(f'\n{name}:\n{dataframe}')


print_data('Resources', resources)
print_data('Contracts', contracts)
print_data('Facilities', facilities)
print_data('Trade', trade)

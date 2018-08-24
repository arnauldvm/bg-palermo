#!/usr/bin/env python3

from os import path
import inspect

scriptdir = path.dirname(inspect.getfile(inspect.currentframe()))

exec(open(path.join(scriptdir, 'load-data.py')).read())

def print_data(name, dataframe):
	print(f'\n{name}:\n{dataframe}')

print_data('Resources', resources)
print_data('Contracts', contracts)
print_data('Facilities', facilities)
print_data('Trade', trade)

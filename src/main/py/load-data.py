#!/usr/bin/env python2

from os import path
import inspect

scriptdir = path.dirname(inspect.getfile(inspect.currentframe()))
srcdir = path.normpath(path.join(scriptdir, '..', '..'))
datadir = path.normpath(path.join(srcdir, 'main', 'data'))

import pandas as pd

resources = pd.read_csv(path.join(datadir, 'resources.csv'), delim_whitespace=True, skiprows=[1])
resources.set_index('color_en', inplace=True, drop=False)
print resources
colors = resources.color_en

contracts = pd.read_csv(path.join(datadir, 'contracts.csv'), delim_whitespace=True, skiprows=[1])
contracts['shipping'] = [
    { color: row[color] for color in colors if row[color]!=0 }
    for index, row in contracts.iterrows()
]
contracts.drop(columns=colors, inplace=True)
contracts.set_index('kind', inplace=True)
print contracts

facilities = pd.read_csv(path.join(datadir, 'facilities.csv'), delim_whitespace=True, skiprows=[1])
facilities['nature'] = [
    [ color for color in colors if row[color]=='y' ]
    for index, row in facilities.iterrows()
]
facilities.drop(columns=colors, inplace=True)
facilities.set_index('type', inplace=True)
print facilities

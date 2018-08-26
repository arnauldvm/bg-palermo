#!/usr/bin/env python3

from os import path
import inspect

if not 'scriptdir' in globals(): scriptdir = path.dirname(inspect.getfile(inspect.currentframe()))
srcdir = path.normpath(path.join(scriptdir, '..', '..'))
datadir = path.normpath(path.join(srcdir, 'main', 'data'))

import pandas as pd

def read_data(name):
	return pd.read_csv(path.join(datadir, name+'.csv'), delim_whitespace=True, skiprows=[1])

resources = read_data('resources')
resources.set_index('color_en', inplace=True, drop=False)
colors = resources.color_en

contracts = read_data('contracts')
contracts['shipping'] = [
	{ color: row[color] for color in colors if row[color]!=0 }
	for index, row in contracts.iterrows()
]
contracts.drop(columns=colors, inplace=True)
contracts.set_index('kind', inplace=True)

facilities = read_data('facilities')
facilities['nature'] = [
	[ color for color in colors if row[color]=='y' ]
	for index, row in facilities.iterrows()
]
facilities.drop(columns=colors, inplace=True)
facilities.set_index('type', inplace=True)

trade = read_data('trade')
# trade.set_index('offer', inplace=True, drop=True)
# trade = trade.transpose(copy=False)
# intervals = trade.columns
# trade['price'] = [
# 	{ pd.Interval(*(map(int, interval.split("-"))), closed='both'): row[interval] for interval in intervals }
# 	for index, row in trade.iterrows()
# ]
# trade.drop(columns=intervals, inplace=True)
trade.set_index(pd.IntervalIndex.from_tuples([ tuple(map(int, interval.split("-"))) for interval in trade.offer ], closed='both'), inplace=True)
trade.drop(columns='offer', inplace=True)
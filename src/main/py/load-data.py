#!/usr/bin/env python 2

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
print " ".join(colors)

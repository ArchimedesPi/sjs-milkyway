import re
from io import StringIO

import pandas as pd

def load_cybspect(file):
    with open(file) as f:
        raw_file = f.read()
        trimmed = re.sub(r'(?m)^#\s*.+\s*$', '', raw_file).lstrip('\n')
        trimmed = re.sub(r'(?m)^\s+', '', trimmed)
        trimmed = "\t\tXL1\tYR1\tFreq2(MHz)\tXL2\tYR2\n" + trimmed

        dat = pd.read_table(StringIO(trimmed), sep='\s+', index_col=0,
                            usecols=['XL1']).sort_index()
        return dat
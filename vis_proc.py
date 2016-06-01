import sys
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from detect_peaks import detect_peaks
from load_cybspect import load_cybspect

def show_peaks(datum):
    spect = load_cybspect(datum['file'])
    spect_roi = spect['XL1'][1420:1421]
    raw_x = spect_roi.index
    raw_y = spect_roi.values

    s = UnivariateSpline(raw_x, raw_y, s=1)
    # resample
    sx = np.linspace(raw_x.min(), raw_x.max(), num=len(raw_x)*5)
    sy = s(sx)

    peaks_x, peaks_y = zip(*datum['peaks'])

    plt.plot(raw_x, raw_y, '--')
    plt.plot(sx, sy, '-')
    plt.scatter(peaks_x, peaks_y, s=60, marker='+', color='red')
    plt.show()

with open('processmanifest.json') as f:
    manifest = json.load(f)
    for datum in manifest:
        show_peaks(datum)

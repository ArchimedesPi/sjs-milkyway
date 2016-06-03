import sys
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from detect_peaks import detect_peaks
from load_cybspect import load_cybspect

def plot_peaks(datum):
    spect = load_cybspect(datum['file'])
    spect_roi = spect['XL1'][1420-0.75:1420+0.75]
    raw_x = spect_roi.index
    raw_y = spect_roi.values

    s = UnivariateSpline(raw_x, raw_y, s=1)
    # resample
    sx = np.linspace(raw_x.min(), raw_x.max(), num=len(raw_x)*5)
    sy = s(sx)

    peaks_x, peaks_y = zip(*datum['peaks'])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(raw_x, raw_y, '--')
    ax.plot(sx, sy, '-')
    ax.scatter(peaks_x, peaks_y, s=60, marker='+', color='red')

    return fig

if __name__ == "__main__":
    with open('processmanifest.json') as f:
        manifest = json.load(f)
        for datum in manifest[0:5]:
            plot_peaks(datum).show()

    plt.show()
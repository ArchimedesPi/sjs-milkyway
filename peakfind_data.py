import sys
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import peakutils.peak

from detect_peaks import detect_peaks
from load_cybspect import load_cybspect

def find_peaks(spectrum_slice):
    raw_x = spectrum_slice.index
    raw_y = spectrum_slice.values

    s = UnivariateSpline(raw_x, raw_y, s=1)
    # resample
    sx = np.linspace(raw_x.min(), raw_x.max(), num=len(raw_x)*5)
    sy = s(sx)

    # peak_indices = detect_peaks(sy, edge='rising',
                                # kpsh=True, threshold=2, show=True)
    peak_indices = detect_peaks(sy, mph=720, kpsh=True)
    # peak_indices = peakutils.peak.indexes(sy, min_dist=10)
    peaks_x = [sx[i] for i in peak_indices]
    peaks_y = [sy[i] for i in peak_indices]

    # plt.plot(raw_x, raw_y, '--')
    # plt.plot(sx, sy, '-')
    # plt.scatter(peaks_x, peaks_y, s=60, marker='+', color='red')
    # plt.show()

    return list(zip(peaks_x, peaks_y))


if __name__ == "__main__":
    pmanifest = []

    with open('datamanifest.json') as f:
        manifest = json.load(f)

        for datum in manifest:
            print(datum)

            spect = load_cybspect(datum['file'])
            spect_roi = spect['XL1'][1420:1421]
            datum['peaks'] = find_peaks(spect_roi)
            datum['processed'] = True
            datum['approved'] = None

            pmanifest.append(datum)

    with open('processmanifest.json', 'w') as f:
        json.dump(pmanifest, f, sort_keys=True, indent=2)
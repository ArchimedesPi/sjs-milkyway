repeakfind = """LACH-CC-239
LACH-CC-238
LACH-CC-237
LACH-CC-242
LACH-CC-236
LACH-CC-235
LACH-CC-234
LACH-CC-233
LACH-CC-232
LACH-CC-231
LACH-CC-230
LACH-CC-229
LACH-CC-228
LACH-CC-227
LACH-CC-226
LACH-CC-225
LACH-CC-224
LACH-CC-223
LACH-CC-222
LACH-CC-245
LACH-CC-221
LACH-CC-220
LACH-CC-219
LACH-CC-218
LACH-CC-217
LACH-CC-216
LACH-CC-215
LACH-CC-214
LACH-CC-213
LACH-CC-212
LACH-CC-211
LACH-CC-210
LACH-HHG-246"""

import json

from peakfind_data import find_peaks
from load_cybspect import load_cybspect

pmanifest = []

with open('datamanifest.json') as f:
    manifest = json.load(f)

    for obsname in repeakfind.split('\n'):
        datum = [x for x in manifest if x['obsname'] == obsname][0]
        print(datum)

        spect = load_cybspect(datum['file'])
        centerfreq = 1420
        spect_roi = spect['XL1'][centerfreq-1.5:centerfreq+1.5]
        datum['peaks'] = find_peaks(spect_roi)
        datum['processed'] = True
        datum['approved'] = None

        pmanifest.append(datum)

with open('repeakfindmanifest.json', 'w') as f:
    json.dump(pmanifest, f, sort_keys=True, indent=2)

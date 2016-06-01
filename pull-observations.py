#!/usr/bin/env python3

# quick script to find missing observations in our 360deg observation program
# on the 20m green bank radio telescope

import json
import re
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import sys

from colorama import Fore, Back, Style

OBS_REGEX = r'LACH-?([A-Za-z]+)-?(\d+)(-\d+)?'

print(Fore.GREEN + "Loading NRAO 20m log data")
with open('./nrao-log.html') as f:
    log_html = f.read()

print(Fore.MAGENTA + "Parsing HTML with BeautifulSoup4")
log_soup = BeautifulSoup(log_html, 'html5lib')

observation_tags = [tag.find('a') for tag in log_soup.find_all('li')]
observations = [tag.string.strip() for tag in observation_tags]

our_obs = [re.sub(r'\.htm$', '', o) for o in observations
                if re.match(OBS_REGEX+r'/\S*', o)]

manifest = []

for obs in our_obs:
    obs_url = 'http://www.gb.nrao.edu/20m/peak/' + obs + '.spect.cyb.txt'
    obs_matches = re.match(OBS_REGEX+r'/\S*', obs)
    obs_file = 'data/' + 'LACH-' + obs_matches.group(1) + '-' + obs_matches.group(2) + '.spect.cyb.txt'

    manifest.append({'lat': 0, 'lon': int(obs_matches.group(2)),
                     'observer': obs_matches.group(1),
                     'file': obs_file,
                     'processed': False})

    print(Fore.GREEN + Style.BRIGHT + ("Downloading %s" % obs) + Style.RESET_ALL)

    r = requests.get(obs_url, stream=True)
    total_len = int(r.headers.get('content-length'))

    with open(obs_file, 'wb') as f:
        for data in tqdm(r.iter_content(chunk_size=1024), total=(total_len/1024)+1):
            f.write(data)

with open('datamanifest.json', 'w') as f:
    f.write(json.dumps(manifest, sort_keys=True, indent=2))

sys.stdout.write(Style.RESET_ALL)


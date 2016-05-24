#!/usr/bin/env python3

# quick script to find missing observations in our 360deg observation program
# on the 20m green bank radio telescope

import json
import re
from bs4 import BeautifulSoup

from colorama import Fore, Back, Style

OBS_REGEX = r'LACH-?(\w+)-?(\d+)'

print(Fore.GREEN + "Loading NRAO 20m log data")
with open('./nrao-log.html') as f:
    log_html = f.read()

print(Fore.MAGENTA + "Parsing HTML with BeautifulSoup4")
log_soup = BeautifulSoup(log_html, 'html5lib')

observation_tags = [tag.find('a') for tag in log_soup.find_all('li')]
observations = [tag.string.strip() for tag in observation_tags]
observation_names = [re.search(r'^(\S*)/\S*', obs).group(1) for obs in observations]

covered_lats = [int(re.match(OBS_REGEX, o).group(2)) for o in observation_names
                if re.match(OBS_REGEX, o)]

if len(covered_lats) == len(set(covered_lats)):
    print(Fore.GREEN + "No duplicate LACH observations")
else:
    print(Fore.YELLOW + "Duplicate LACH observations found! Duplicates:")
    print([x for x in covered_lats if covered_lats.count(x) > 1])

uncompleted_obs = set(range(0, 360 + 1)) - set(covered_lats)
if len(uncompleted_obs) > 0:
    print(Fore.YELLOW + "Uncompleted observations:")
    print(uncompleted_obs)

import json
import re

with open('datamanifest.json') as f:
	manifest = json.load(f)
	for datum in manifest:
		with open(datum['file']) as f:
			datafile = f.read()
			datematch = re.search('(?m)^#\s+DATE_OBS=(\S+)', datafile).group(1)
			ramatch = re.search('(?m)^#\s+RA=(\S+)', datafile).group(1)
			decmatch = re.search('(?m)^#\s+DEC=(\S+)', datafile).group(1)

			datum['ra'] = ramatch
			datum['dec'] = decmatch

			datum['date'] = datematch.split('T')[0]
			datum['time'] = datematch.split('T')[1]

with open('datamanifest.json', 'w') as f:
	json.dump(manifest, f, sort_keys=True, indent=2)

import sys
import json
import requests
from bs4 import BeautifulSoup

def get_vlsrk(date, time, ra, dec):
	r = requests.get('http://wwwlocal.gb.nrao.edu/cgi-bin/radvelcalc.py',
		{'UTDate': date.split('.')[0].replace('-', '/'),
		'UTTime': time,
		'RA': ra,
		'DEC': dec})
	s = BeautifulSoup(r.text, 'lxml')
	return float(s.find_all('td')[5].text.strip().split(' ')[0])

if __name__ == "__main__":
	with open(sys.argv[1]) as f:
		manifest = json.load(f)
		for datum in manifest:
			datum['v_lsrk'] = get_vlsrk(datum['date'],
				datum['time'],
				datum['ra'],
				datum['dec'])
			print("%s: v_lsrk = %s" % (datum['obsname'], datum['v_lsrk']))

	with open(sys.argv[1], 'w') as f:
		json.dump(manifest, f)

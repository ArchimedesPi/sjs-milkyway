from io import BytesIO
import json

from flask import Flask, render_template, send_file, request, redirect, url_for, session

import matplotlib
matplotlib.use('Agg')

from vis_proc import plot_peaks

app = Flask(__name__)
app.secret_key = '|IBq\xd5$\x9f\x9f4MLG\x7f\xea\xdb\x98K\x93\xb1Ay\xa3\xe5\xaa'

with open('approvalmanifest.json') as f:
    manifest = json.load(f)

@app.route('/figure/<observation_name>.png')
def figure(observation_name):
    with open('approvalmanifest.json') as f:
        manifest = json.load(f)
        datum = [x for x in manifest if x['obsname'] == observation_name][0]
        figure = plot_peaks(datum)

    image = BytesIO()
    figure.savefig(image, format='png')
    image.seek(0)
    return send_file(image, mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        datum = [x for x in manifest if x['obsname'] == request.form['obsname']][0]
        if request.form['correctness'] == 'correct':
            datum['approved'] = True
        elif request.form['correctness'] == 'incorrect':
            datum['approved'] = False

        with open('approvalmanifest.json', 'w') as g:
            json.dump(manifest, g, sort_keys=True, indent=2)
        
        return redirect(url_for('root'))
    else:
        # find the first unapproved datum
        datum = [x for x in manifest if x['approved'] == None][0]

        return render_template('index.html',
            peakdatum=datum)

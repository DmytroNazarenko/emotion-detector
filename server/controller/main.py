# main.py
import json
import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask import current_app as app
from werkzeug.utils import secure_filename

from server.controller.nn_tools import get_predictions

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            summary = get_predictions(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('main.upload_summary',
                                    summary=summary))
    return render_template('index.html')


@main.route('/upload_summary/<string:summary>')
@login_required
def upload_summary(summary):
    j = json.loads(summary)
    neutral = j['counts']['0']
    happy = j['counts']['1']
    sad = j['counts']['2']
    hate = j['counts']['3']
    anger = j['counts']['4']
    print(j['means'])
    return render_template('summary.html', happy=happy, neutral=neutral, sad=sad,hate=hate, anger=anger, g=j['means'][0])
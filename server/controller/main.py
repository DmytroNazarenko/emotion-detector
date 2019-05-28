# main.py
import json
import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_manager
from flask import current_app as app
from sqlalchemy import select
from werkzeug.utils import secure_filename

from server.controller.nn_tools import get_predictions
from server.model.models import Summary, SampleSummary
from server import db

from flask import g

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/upload_file', methods=['POST'])
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
                                    summary=summary, filename=filename))
    return render_template('index.html')


@main.route('/upload_file', methods=['GET'])
@login_required
def load_summary():
    id = current_user.id
    summary = Summary.query.filter_by(user_id=id).all()
    return render_template('index.html', summary=summary)


@main.route('/upload_summary/<string:summary>/<string:filename>')
@login_required
def upload_summary(summary, filename):
    j = json.loads(summary)
    emotions=['neutral', 'happy', 'sad', 'hate', 'anger']
    neutral = j['counts']['0']
    happy = j['counts']['1']
    sad = j['counts']['2']
    hate = j['counts']['3']
    anger = j['counts']['4']
    pr = j['predictions']
    # pr = prs[0]
    # TODO user_id
    new_summary = Summary(user_id=3,name=filename, hate_cnt=hate, neutal_cnt=neutral, happy_cnt=happy, sad_cnt=sad, anger_cnt=anger)
    db.session.add(new_summary)
    db.session.commit()
    print(new_summary.id)
    print(pr)
    for i in range(len(pr)):
        new_sample_summary = SampleSummary(summary_id=new_summary.id, neutral=pr[i][0][0],
                                           happy=pr[i][0][1], sad=pr[i][0][2], hate=pr[i][0][3], anger=pr[i][0][4])
        db.session.add(new_sample_summary)
    db.session.commit()
    return render_template('summary.html', emotions=emotions, happy=happy, neutral=neutral, sad=sad,hate=hate, anger=anger, pr=pr)

@main.route('/load_summary_by_id/<int:id>')
@login_required
def load_summary_by_id(id):
    j = Summary.query.filter_by(id=id).all()
    emotions=['neutral', 'happy', 'sad', 'hate', 'anger']
    neutral = j['counts']['0']
    happy = j['counts']['1']
    sad = j['counts']['2']
    hate = j['counts']['3']
    anger = j['counts']['4']
    pr = SampleSummary.query.filter_by(summary_id=id).all()
    return render_template('summary.html', emotions=emotions, happy=happy, neutral=neutral, sad=sad,hate=hate, anger=anger, pr=pr)
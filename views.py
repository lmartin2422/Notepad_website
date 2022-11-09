# views stores the standard routes for the website (any page user can visit)

from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash  # to display messages to the user
from flask_login import login_required
from flask_login import current_user  # detects if user is logged in or not then provides info
from .models import Note
from . import db
import json
from flask import jsonify


views = Blueprint('views', __name__)  # sets up a blueprint for our flask application


@views.route('/', methods=['GET', 'POST'])  # defines and runs the home page of the website
@login_required  # can't access the homepage unless you are logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)  # checks for if current user is authenticated


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # takes request id
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:  # if there is a note
        if note.user_id == current_user.id:  # if the user is signed in
            db.session.delete(note)  # delete the note
            db.session.commit()

    return jsonify({})


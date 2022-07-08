import json
from curses import flash
from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import JSON
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', "POST"])
@login_required
def home():

    if request.method == "POST":
        # User is adding a new note
        note = request.form.get('note') # Get note data from form

        if len(note) < 1:
            flash("Note must be at least 1 character", category='error')
        else:
            # Add note to user's notes
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category='success')

    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    """ This function deletes the note specified in the POST request

    :return: empty response
    :rtype: dict
    """
    data = json.loads(request.data)
    note_id = data["noteId"]

    note = Note.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            # Delete note if it belongs to the current user
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) # Return empty response to request

import shutil
from pathlib import Path

import eyed3
import sqlalchemy
from flask import Blueprint, render_template, flash, redirect, request, send_file

from taggedMp3.config import Config
from taggedMp3.utils import save_file

template_bp = Blueprint('template_bp', __name__)


@template_bp.route('/', methods=['GET'])  # index route
def index():
    return render_template('index.html')


@template_bp.route('/', methods=['POST'])
def upload_song():
    status, *data = save_file()
    data = data[0]
    if status == 400:
        flash(data)
        return redirect(request.url)
    for token in data['tokens']:  # flashing tokens to use in html file
        print("flashing")
        flash(token)
    return render_template('edit.html', song_id=data['id'])  # responding with edit screen


@template_bp.route('/edit/<string:id>', methods=['POST'])
def edit(id=None):
    if request.method == 'POST':  # POST is activated on save button click
        new_title = request.form['title']  # getting applied song tags
        new_artist = request.form['artist']
        new_album = request.form['album']
        audio_file = Config['UPLOAD_FOLDER'] + '/' + id + '.mp3'  # getting file name
        song = eyed3.load(audio_file).tag  # loading mp3 file
        song.title = new_title  # setting new tags
        song.artist = new_artist
        song.album = new_album
        song.save()  # saving mp3 file
        if new_title is not None and new_artist is not None:  # if the user provided title and artist we rename the file
            new_name = Path.cwd() / Config['UPLOAD_FOLDER'] / f'{new_artist}-{new_title}.mp3'
            if new_album is None:
                new_album = ''
            try:
                # song = Song(id=id, title=new_title, artist=new_artist, album=new_album)
                # db.session.add(song)
                # db.session.commit()
                shutil.copy(audio_file, new_name)
            except sqlalchemy.exc.IntegrityError:
                print("File exists")
            audio_file = new_name
        return send_file(audio_file, as_attachment=True)  # sending the file to user

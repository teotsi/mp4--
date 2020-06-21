import os
import re
import shutil
from pathlib import Path

import eyed3
import moviepy.editor as mp
import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists

from taggedMp3.utils import valid_file_extension, md5

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'  # sqlite .db file location
    app.config['UPLOAD_FOLDER'] = 'static/files'
    app.secret_key = "qwerty"
    db.init_app(app)
    with app.app_context():
        import taggedMp3.model
        db.create_all()
        from .model import File, Song

    @app.route('/', methods=['GET'])  # index route
    def index():
        return render_template('index.html')

    @app.route('/', methods=['POST'])
    def upload_song():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = file.filename
            if valid_file_extension(filename):
                if not os.path.exists(app.config['UPLOAD_FOLDER']):  # creating file upload folder if it doesn't exist
                    File.query.delete()
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(full_file_path)  # saving file
                mixed_song_name = filename.split('.')[0]  # removing file extension
                print(mixed_song_name)
                tokens = re.split('[_-]', mixed_song_name)  # creating possible tokens
                print(tokens)
                for token in tokens:  # flashing tokens to use in html file
                    print("flashing")
                    flash(token)
                audio_file_id = md5(full_file_path)  # creating unique id
                audio_file = app.config['UPLOAD_FOLDER'] + '/' + audio_file_id + '.mp3'
                print(audio_file)
                print(filename)
                if not db.session.query(exists().where(File.id == audio_file_id)).scalar():
                    clip = mp.VideoFileClip(app.config['UPLOAD_FOLDER'] + '/' + filename)  # reading video file
                    clip.audio.write_audiofile(audio_file)  # extracting audio file
                    file = File(id=audio_file_id)
                    db.session.add(file)
                    db.session.commit()
                    print("added new id")
                else:
                    print("File already exists!")
                print("moving on")
                return render_template('edit.html', song_id=audio_file_id)  # responding with edit screen
            else:
                flash("invalid extension")
                return redirect(request.url)

    @app.route('/edit/<string:id>', methods=['POST'])
    def edit(id=None):
        if request.method == 'POST':  # POST is activated on save button click
            new_title = request.form['title']  # getting applied song tags
            new_artist = request.form['artist']
            new_album = request.form['album']
            audio_file = app.config['UPLOAD_FOLDER'] + '/' + id + '.mp3'  # getting file name
            song = eyed3.load(audio_file).tag  # loading mp3 file
            song.title = new_title  # setting new tags
            song.artist = new_artist
            song.album = new_album
            song.save()  # saving mp3 file
            if new_title is not None and new_artist is not None:  # if the user provided title and artist we rename the file
                new_name = Path.cwd() / app.config['UPLOAD_FOLDER'] / f'{new_artist}-{new_title}.mp3'
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

    return app

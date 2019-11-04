import hashlib
import os
import re
import shutil

import eyed3
import moviepy.editor as mp
import sqlalchemy
from flask import Flask, render_template, request, redirect, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'  # sqlite .db file location
app.config['UPLOAD_FOLDER'] = 'static/files'
app.secret_key = "qwerty"
extensions = ['mp4', 'avi']
db = SQLAlchemy(app)  # initialising database


class Song(db.Model):  # declaring a new class that will be used as a table
    id = db.Column(db.String(20), db.ForeignKey('file.id'), nullable=False, primary_key=True)
    title = db.Column(db.String(120), nullable=False, primary_key=True)
    artist = db.Column(db.String(120), nullable=False, primary_key=True)
    album = db.Column(db.String(120), nullable=False, primary_key=True)

    def __repr__(self):
        return self.id + ", " + self.title + ", " + self.artist + ", " + self.album


class File(db.Model):
    id = db.Column(db.String(20), primary_key=True)

    def __repr__(self):
        return self.id


def md5(fname):  # used to calculate md5 checksum for file
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def valid_file_extension(filename):  # checking if file is a video file
    if '.' in filename:
        if filename.split('.')[-1] in extensions:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])  # index route
def index():
    if request.method == 'POST':  # POST is activated on file upload
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
    else:
        return render_template('index.html')


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
            new_name = app.config['UPLOAD_FOLDER'] + '/' + new_artist + '-' + new_title + '.mp3'
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


if __name__ == '__main__':  # initializing app
    app.run()

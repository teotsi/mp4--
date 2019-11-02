import hashlib
import os
import re
import shutil

import eyed3
import moviepy.editor as mp
from flask import Flask, render_template, request, redirect, flash, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.secret_key = "qwerty"
extensions = ['mp4', 'avi', 'mp3']


def valid_file_extension(filename):
    if '.' in filename:
        if filename.split('.')[-1] in extensions:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                mixed_song_name = filename.split('.')[0]
                print(mixed_song_name)
                tokens = re.split('[_-]', mixed_song_name)
                print(tokens)
                for token in tokens:
                    print("flashing")
                    flash(token)
                audio_file_id = hashlib.md5(
                    (mixed_song_name + str(request.cookies.get('filesize'))).encode()).hexdigest()
                audio_file = app.config['UPLOAD_FOLDER'] + '/' + audio_file_id + '.mp3'
                print(audio_file)
                print(filename)
                clip = mp.VideoFileClip(app.config['UPLOAD_FOLDER'] + '/' + filename)
                clip.audio.write_audiofile(audio_file)
                print("moving on")
                return render_template('edit.html', song_id=audio_file_id)
            else:
                flash("invalid extension")
                return redirect(request.url)
    else:
        return render_template('index.html')


@app.route('/edit/<string:id>', methods=['POST'])
def edit(id=None):
    if id == None:
        return "hehehehehe"
    if request.method == 'POST':
        new_title = request.form['title']
        new_artist = request.form['artist']
        new_album = request.form['album']
        audio_file = app.config['UPLOAD_FOLDER'] + '/' + id + '.mp3'
        song = eyed3.load(audio_file).tag
        song.title = new_title
        song.artist = new_artist
        song.album = new_album
        song.save()
        if new_title is not None and new_artist is not None:
            new_name = app.config['UPLOAD_FOLDER'] + '/' + new_artist + '-' + new_title + '.mp3'
            shutil.copy(audio_file, new_name)
            audio_file = new_name
        return send_file(audio_file, as_attachment=True)


if __name__ == '__main__':
    app.run()

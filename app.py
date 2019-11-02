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
extensions = ['mp4', 'avi']


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
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # saving file
                mixed_song_name = filename.split('.')[0]  # removing file extension
                print(mixed_song_name)
                tokens = re.split('[_-]', mixed_song_name)  # creating possible tokens
                print(tokens)
                for token in tokens:  # flashing tokens to use in html file
                    print("flashing")
                    flash(token)
                audio_file_id = hashlib.md5(  # creating a unique file id for uploaded file based on file size
                    (mixed_song_name + str(request.cookies.get('filesize'))).encode()).hexdigest()
                audio_file = app.config['UPLOAD_FOLDER'] + '/' + audio_file_id + '.mp3'
                print(audio_file)
                print(filename)
                clip = mp.VideoFileClip(app.config['UPLOAD_FOLDER'] + '/' + filename)  # reading video file
                clip.audio.write_audiofile(audio_file)  # extracting audio file
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
            shutil.copy(audio_file, new_name)
            audio_file = new_name
        return send_file(audio_file, as_attachment=True)  # sending the file to user


if __name__ == '__main__':  # initializing app
    app.run()

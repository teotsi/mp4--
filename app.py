import os

import eyed3
import moviepy.editor as mp
from flask import Flask, render_template, request, redirect, flash, jsonify, make_response, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'
app.secret_key = "qwerty"
extensions = ['mp4', 'avi', 'mp3']
audio_file = ''


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
            filename = secure_filename(file.filename)
            if valid_file_extension(filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                global audio_file
                audio_file = filename.split('.')[0] + '.mp3'
                clip = mp.VideoFileClip(filename)
                clip.audio.write_audiofile(audio_file)
                audiofile = eyed3.load(audio_file)
                flash(audiofile.tag.title)
                flash(audiofile.tag.artist)
                flash(audiofile.tag.album)
                print("moving on")
                return render_template('edit.html')
            else:
                flash("invalid extension")
                return redirect(request.url)
    else:
        return render_template('index.html')


@app.route('/edit', methods=['POST'])
def edit():
    print("hey")
    if request.method == 'POST':
        new_title = request.form['title']
        new_artist = request.form['artist']
        new_album = request.form['album']
        song = eyed3.load(audio_file).tag
        song.title = new_title
        song.artist = new_artist
        song.album = new_album
        song.save()
        return make_response(jsonify({"message": "File uploaded"}), 200)


if __name__ == '__main__':
    app.run()

import os

from flask import Flask, render_template, request, redirect, flash
import eyed3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'
app.secret_key = "qwerty"


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            audiofile = eyed3.load("/home/p3160180/Downloads/test.mp3")
            flash(audiofile.tag.title)
            flash(audiofile.tag.artist)
            flash(audiofile.tag.album)
            return render_template('edit.html')
    else:
        return render_template('index.html')


@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        new_title = request.form['title']
        new_artist = request.form['artist']
        new_album = request.form['album']
        print("yeaaaaaaaaheeee")
        return new_artist


if __name__ == '__main__':
    app.run()

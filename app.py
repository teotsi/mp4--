import os

from flask import Flask, render_template, request, redirect, flash
import eyed3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'
app.secret_key = "secret key"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("holaaa")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            print("hey")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

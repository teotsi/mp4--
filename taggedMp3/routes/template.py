from flask import Blueprint, render_template, flash, redirect, request, send_file

from taggedMp3.utils import save_file, edit_audio_file

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
    print(data['id'])
    return render_template('edit.html', song_id=data['id'])  # responding with edit screen


@template_bp.route('/edit/<string:id>', methods=['POST'])
def edit(id=None):
    return send_file(str(edit_audio_file(id)), as_attachment=True)  # sending the file to user

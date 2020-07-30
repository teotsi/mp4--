from flask import Blueprint, jsonify, send_from_directory

from taggedMp3.utils import save_file, edit_audio_file

api_bp = Blueprint('api_bp', __name__, url_prefix='/api/')


@api_bp.route('/', methods=['GET'])
def get_index():
    return jsonify({'info': 'just go'})


@api_bp.route('/', methods=['POST'])
def post_file():
    status, *data = save_file()
    data = data[0]
    if status == 400:
        return jsonify({'message': data}), status
    return jsonify(data)


@api_bp.route('/edit/<string:id>', methods=['POST'])
def edit(id=None):
    file_name = f'{id}.mp3'
    return send_from_directory(str(edit_audio_file(id).parent), file_name)  # sending the file to user

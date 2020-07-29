from flask import Blueprint, jsonify

from taggedMp3.utils import save_file

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

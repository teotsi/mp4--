import re
from pathlib import Path

import moviepy.editor as mp
from flask import request
from sqlalchemy import exists

from taggedMp3 import db
from taggedMp3.config import Config
from taggedMp3.model import File
from taggedMp3.utils import valid_file_extension, md5


def save_file():
    if 'file' not in request.files:
        return 400, 'no file found'
    file = request.files['file']
    if file.filename == '':
        return 400, 'filename error'
    if file:
        file_name = file.filename
        if valid_file_extension(file_name):
            full_file_path = Path(Config.UPLOAD_FOLDER) / file_name
            file.save(str(full_file_path))  # saving file
            clean_file_name = file_name.split('.')[0]
            tokens = re.split('[_-]', clean_file_name)  # creating possible tokens
            audio_file_checksum = md5(full_file_path)  # creating unique id
            audio_file_name = Path(Config.UPLOAD_FOLDER) / f'{audio_file_checksum}.mp3'
            if not db.session.query(exists().where(File.id == audio_file_checksum)).scalar():
                clip = mp.VideoFileClip(str(Path(Config.UPLOAD_FOLDER) / file_name))  # reading video file
                clip.audio.write_audiofile(str(audio_file_name))  # extracting audio file
                file = File(id=audio_file_checksum)
                db.session.add(file)
                db.session.commit()
            return 200, {'id': audio_file_checksum, 'tokens': tokens}
    return 400, 'file error'

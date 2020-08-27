import re
import shutil
from pathlib import Path

import eyed3
import moviepy.editor as mp
import sqlalchemy
from flask import request
from sqlalchemy import exists

from taggedMp3 import db
from taggedMp3.config import Config
from taggedMp3.model import File
from taggedMp3.utils import valid_file_extension, md5

SUPPORTED_TAGS=['title','artist','album']

def save_file():
    print(get_request_data(request))
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


def edit_audio_file(id):
    data = get_request_data(request)

    audio_file = Path(Config.UPLOAD_FOLDER) / f'{id}.mp3'  # getting file name
    song = eyed3.load(str(audio_file)).tag  # loading mp3 file
    
    for tag in SUPPORTED_TAGS:
        new_value = data.get(tag)
        if new_value:
            song.__setattr__(tag,new_value)        
    
    song.save()  # saving mp3 file

    new_title = data.get('title')
    new_artist = data.get('artist')

    if new_title is not None and new_artist is not None:  # if the user provided title and artist we rename the file
        new_name = Path.cwd() / Config.UPLOAD_FOLDER / f'{new_artist}-{new_title}.mp3'
        try:
            # song = Song(id=id, title=new_title, artist=new_artist, album=new_album)
            # db.session.add(song)
            # db.session.commit()
            shutil.copy(str(audio_file), str(new_name))
        except sqlalchemy.exc.IntegrityError:
            print("File exists")
    else:
        new_name = Path.cwd() / Config.UPLOAD_FOLDER / f'{id}.mp3'
    audio_file = new_name
    return audio_file.parent, audio_file.name


def get_request_data(request):
    data = request.get_json()
    if not data:
        try:
            return request.form
        except IndexError:
            return {}
    return data

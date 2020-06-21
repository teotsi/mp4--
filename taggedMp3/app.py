import hashlib
import os
import re
import shutil

import eyed3
import moviepy.editor as mp
import sqlalchemy
from flask import Flask, render_template, request, redirect, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists

from taggedMp3.model import File

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'  # sqlite .db file location
app.config['UPLOAD_FOLDER'] = 'static/files'
app.secret_key = "qwerty"
extensions = ['mp4', 'avi']
db = SQLAlchemy(app)  # initialising database




if __name__ == '__main__':  # initializing app
    app.run()

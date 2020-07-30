class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/files'
    SECRET_KEY = 'qwerty'

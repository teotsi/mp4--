import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from taggedMp3.utils import valid_file_extension, md5

db = SQLAlchemy()


def create_app():
    try:
        os.remove(Path.cwd() / 'taggedMp3'/'site.db')
    except OSError:
        pass
    app = Flask(__name__)
    app.config.from_object('taggedMp3.config.Config')
    db.init_app(app)
    with app.app_context():
        import taggedMp3.model
        db.create_all()
        from .model import File, Song
        if not os.path.exists(app.config['UPLOAD_FOLDER']):  # creating file upload folder if it doesn't exist
            File.query.delete()
            os.makedirs(app.config['UPLOAD_FOLDER'])

    from .routes import api_bp, template_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(template_bp)

    return app

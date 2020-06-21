from taggedMp3 import db


class Song(db.Model):  # declaring a new class that will be used as a table
    id = db.Column(db.String(20), db.ForeignKey('file.id'), nullable=False, primary_key=True)
    title = db.Column(db.String(120), nullable=False, primary_key=True)
    artist = db.Column(db.String(120), nullable=False, primary_key=True)
    album = db.Column(db.String(120), nullable=False, primary_key=True)

    def __repr__(self):
        return self.id + ", " + self.title + ", " + self.artist + ", " + self.album


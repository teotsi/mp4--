from taggedMp3 import db


class File(db.Model):
    id = db.Column(db.String(), primary_key=True)

    def __repr__(self):
        return self.id

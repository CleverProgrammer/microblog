from app import db

# Used WWW SQL Designer tool to sketch my idea
# Link: http://ondras.zarovi.cz/sql/demo/
# Click load and enter: rafeh01
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<user %r>' % (self.nickname)
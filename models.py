from app import db
import datetime

# pylint: disable=no-member
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return f"<Message {self.id}>"
    
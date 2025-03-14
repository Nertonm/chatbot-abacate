from app import db

class ChatResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), unique=True, nullable=False)
    answer = db.Column(db.Text, nullable=False)
from flask import jsonify
from app import db
from sqlalchemy.exc import IntegrityError


class Task(db.Model):
    __tablename__ = "Task"
    id = db.Column(db.String(128), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    def __init__(self, id=None, title=None, description=None, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

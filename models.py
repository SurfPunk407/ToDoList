# models.py
from app import db  # Import db from app.py

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=True)
    task_date = db.Column(db.String(20), nullable=True)

    def __init__(self, task, description=None, priority=None, status=True, task_date=None):
        self.task = task
        self.description = description
        self.priority = priority
        self.status = status
        self.task_date = task_date

    def to_dictionary(self):
        return {
            "id": self.id,
            "task": self.task,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "task_date": self.task_date
        }

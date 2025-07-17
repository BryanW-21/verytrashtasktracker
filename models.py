from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):

    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):

    taskId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), default="")
    user_id = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable=False)

    def __repr__(self):
        return f"<Task {self.name}>"


class TaskProgress(db.Model):
    __tablename__ = 'task_progress'

    progressId = db.Column(db.Integer, primary_key=True)
    taskId = db.Column(db.Integer, db.ForeignKey('task.taskId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    task = db.relationship('Task', back_populates='progress')
    user = db.relationship('User', back_populates='task_progress')

Task.progress = db.relationship('TaskProgress', back_populates='task', cascade='all, delete')
User.task_progress = db.relationship('TaskProgress', back_populates='user', cascade='all, delete')
from flask import Flask, render_template, request, jsonify, g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Task, User  # Import models
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Qwerty123456!@127.0.0.1:3306/sdp_project"
app.config['SECRET_KEY'] = "your_secret_key"
app.config['JWT_SECRET_KEY'] = "your_jwt_secret_key"

# Initialize database and JWT
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and issue a JWT token.
    """
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.userId)
    return jsonify({"message": "Login successful", "access_token": access_token}), 200


@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task.
    """
    user_id = get_jwt_identity()
    data = request.json

    if not all(k in data for k in ('name', 'description', 'points')):
        return jsonify({"error": "Missing required fields"}), 400

    new_task = Task(
        name=data['name'],
        description=data['description'],
        points=data['points'],
        image_url=data.get('image_url', ''),
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"taskId": new_task.taskId, **data}), 201


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_all_tasks():
    """
    Retrieve all tasks for the logged-in user.
    """
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "taskId": task.taskId,
        "name": task.name,
        "description": task.description,
        "points": task.points,
        "image_url": task.image_url
    } for task in tasks]), 200


@app.route('/tasks/<int:taskId>', methods=['GET'])
@jwt_required()
def get_task(taskId):
    """
    Retrieve a specific task by taskId for the logged-in user.
    """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(taskId=taskId, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "taskId": task.taskId,
        "name": task.name,
        "description": task.description,
        "points": task.points,
        "image_url": task.image_url
    }), 200


@app.route('/tasks/<int:taskId>', methods=['DELETE'])
@jwt_required()
def delete_task(taskId):
    """
    Delete a task by taskId for the logged-in user.
    """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(taskId=taskId, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


@app.route('/tasks/<int:taskId>', methods=['PUT'])
@jwt_required()
def update_task(taskId):
    """
    Update an existing task for the logged-in user.
    """
    user_id = get_jwt_identity()
    data = request.json

    task = Task.query.filter_by(taskId=taskId, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    required_fields = ['name', 'description', 'points']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    for key in ['name', 'description', 'points', 'image_url']:
        if key in data:
            setattr(task, key, data[key])

    db.session.commit()
    return jsonify({"message": "Task updated successfully", "taskId": taskId}), 200


if __name__ == "__main__":
    app.run(debug=True)
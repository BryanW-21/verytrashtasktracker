from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from extensions import db
from models import initialize_database, create_task, get_tasks_by_user, delete_task, update_task_by_id, get_task_by_id
from auth import register_user, login_user
from config import Config
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

with app.app_context():
    initialize_database()

@app.route('/')
def root_render():
    return render_template("home.html")

@app.route('/home')
def home_render():
    return render_template("home.html")

@app.route("/login_register")
def login_register_render():
    return render_template("login_register.html")

@app.route("/index_user")
def index_user_render():
    return render_template("index_user.html")

@app.route("/tasks")
def tasks_render():
    return render_template("tasks.html")

@app.route("/create_task")
def create_task_render():
    return render_template("create_task.html")


@app.route("/login", methods=["OPTIONS"])
def login_preflight():
    """Handles preflight requests for login"""
    response = jsonify({"message": "CORS preflight success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    response, status = login_user(data)
    return jsonify(response), status

@app.route("/api/tasks/create", methods=["POST"])
@jwt_required()
def create_task_api():
    user_id = get_jwt_identity()
    data = request.json
    if not all(k in data for k in ("name", "description", "points")):
        return jsonify({"error": "Missing required fields"}), 400

    create_task(data["name"], data["description"], data["points"], data.get("image_url", ""), user_id)
    return jsonify({"message": "Task created successfully"}), 201

@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_all_tasks_api():
    user_id = get_jwt_identity()
    tasks = get_tasks_by_user(user_id)  

    task_list = []
    for task in tasks:
        task_dict = {
            "taskId": task.taskId,
            "name": task.name,
            "description": task.description,
            "points": task.points,
            "image_url": task.image_url
        }
        task_list.append(task_dict)

    return jsonify(task_list), 200

@app.route("/api/tasks/<int:taskId>", methods=["DELETE"])
@jwt_required()
def delete_task_api(taskId):
    user_id = get_jwt_identity()
    delete_task(taskId, user_id)
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route("/api/tasks/<int:taskId>", methods=["PUT"])
@jwt_required()
def update_task_api(taskId):
    user_id = get_jwt_identity()
    data = request.json

    required_fields = ["name", "description", "points"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    update_task_by_id(taskId, user_id, data["name"], data["description"], data["points"], data.get("image_url", ""))

    return jsonify({"message": "Task updated successfully"}), 200

@app.route("/api/tasks/<int:taskId>", methods=["GET"])
@jwt_required()
def get_task(taskId):
    """Retrieve a specific task by taskId."""
    user_id = get_jwt_identity()  # Get user ID from JWT
    task = get_task_by_id(taskId, user_id)  # Fetch task from database

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "taskId": task.taskId,
        "name": task.name,
        "description": task.description,
        "points": task.points,
        "image_url": task.image_url
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405
if __name__ == "__main__":
    app.run(debug=True)

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response
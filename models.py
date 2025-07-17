from sqlalchemy import text
from extensions import db

def create_tables():
    users_table_sql = text("""
        CREATE TABLE IF NOT EXISTS users (
            userId INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )ENGINE=InnoDB;
    """)

    tasks_table_sql = text("""
        CREATE TABLE IF NOT EXISTS tasks (
            taskId INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            points INT NOT NULL,
            image_url VARCHAR(255) DEFAULT '',
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(userId) ON DELETE CASCADE
        )ENGINE=InnoDB;
    """)

    task_progress_table_sql = text("""
        CREATE TABLE IF NOT EXISTS task_progress (
            progressId INT AUTO_INCREMENT PRIMARY KEY,
            taskId INT NOT NULL,
            userId INT NOT NULL,
            status VARCHAR(50) NOT NULL,
            FOREIGN KEY (taskId) REFERENCES tasks(taskId) ON DELETE CASCADE,
            FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
        )ENGINE=InnoDB;
    """)

    with db.engine.begin() as connection:
        connection.execute(users_table_sql)
        connection.execute(tasks_table_sql)
        connection.execute(task_progress_table_sql)

def initialize_database():
    create_tables()

# User Functions
def create_user(username, email, password_hash):
    sql = text("""
        INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :password_hash)
    """)
    db.session.execute(sql, {"username": username, "email": email, "password_hash": password_hash})
    db.session.commit()

def get_user_by_email(email):
    sql = text("SELECT * FROM users WHERE email = :email")
    result = db.session.execute(sql, {"email": email}).fetchone()
    return result

# Task Functions
def create_task(name, description, points, image_url, user_id):
    sql = text("""
        INSERT INTO tasks (name, description, points, image_url, user_id) 
        VALUES (:name, :description, :points, :image_url, :user_id)
    """)
    db.session.execute(sql, {"name": name, "description": description, "points": points, "image_url": image_url, "user_id": user_id})
    db.session.commit()

def get_tasks_by_user(user_id):
    sql = text("SELECT * FROM tasks WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def delete_task(taskId, user_id):
    sql = text("DELETE FROM tasks WHERE taskId = :taskId AND user_id = :user_id")
    db.session.execute(sql, {"taskId": taskId, "user_id": user_id})
    db.session.commit()

def update_task_by_id(taskId, user_id, name, description, points, image_url):
    sql = text("""
        UPDATE tasks
        SET name = :name, description = :description, points = :points, image_url = :image_url
        WHERE taskId = :taskId AND user_id = :user_id
    """)
    db.session.execute(sql, {
        "taskId": taskId,
        "user_id": user_id,
        "name": name,
        "description": description,
        "points": points,
        "image_url": image_url
    })
    db.session.commit()

def get_task_by_id(taskId, user_id):
    sql = text("SELECT * FROM tasks WHERE taskId = :taskId AND user_id = :user_id")
    result = db.session.execute(sql, {"taskId": taskId, "user_id": user_id}).fetchone()
    return result

def get_user_by_username(username):
    """Fetches a user by username."""
    sql = text("SELECT * FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username": username}).fetchone()
    return result

def get_user_by_email(email):
    """Fetches a user by email."""
    sql = text("SELECT * FROM users WHERE email = :email")
    result = db.session.execute(sql, {"email": email}).fetchone()
    return result

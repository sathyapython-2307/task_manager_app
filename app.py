from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

def ensure_db():
    if not os.path.exists("tasks.db"):
        with app.app_context():
            db.create_all()

@app.route("/")
def index():
    ensure_db()
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks, title="Task Manager")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    ensure_db()
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    ensure_db()
    data = request.get_json()
    if "title" in data:
        task = Task(title=data["title"])
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task added"}), 201
    return jsonify({"message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)

# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  

# Database Configuration (using environment variable)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


from models import Task


from flask import jsonify, request

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([task.to_dictionary() for task in tasks])

    elif request.method == 'POST':
        data = request.get_json()
        new_task = Task(
            task=data['task'],
            description=data.get('description', ''),
            priority=data.get('priority', ''),
            status=data.get('status', True), # Get status, default to True
            task_date=data.get('task_date', '')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dictionary()), 201

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'PUT':
        data = request.get_json()
        task.task = data.get('task', task.task) # Update Task name
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.task_date = data.get('task_date', task.task_date)

        db.session.commit()
        return jsonify(task.to_dictionary())

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

# Create Tables (run once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)  

from flask import jsonify, request
from models import db, Task  # Import db and Task model from models.py
from app import app  # Import the app from the main app.py file to register the routes

# GET and POST methods for tasks
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()  # Fetch all tasks from the database
        return jsonify([task.to_dictionary() for task in tasks])  # Return tasks as JSON

    elif request.method == 'POST':
        data = request.get_json()  # Get the data from the request
        new_task = Task(
            task=data['task'],
            description=data.get('description', ''),
            priority=data.get('priority', ''),
            status=True,  # Default to True for active tasks
            task_date=data.get('task_date', '')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dictionary()), 201  # Return the newly created task

# PUT and DELETE methods for task by id
@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'PUT':
        data = request.get_json()
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify(task.to_dictionary())

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

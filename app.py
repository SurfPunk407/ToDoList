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
        try:
            tasks = Task.query.all()
            return jsonify([task.to_dictionary() for task in tasks])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_task = Task(
                task=data['task'],
                description=data.get('description', ''),
                priority=data.get('priority', ''),
                status=data.get('status', True),
                task_date=data.get('task_date', '')
            )
            db.session.add(new_task)
            db.session.commit()
            return jsonify(new_task.to_dictionary()), 201 
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    try:
        task = Task.query.get_or_404(id)

        if request.method == 'PUT':
            data = request.get_json()
            task.task = data.get('task', task.task)
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'username' not in session:
        logging.warning("Unauthorized access to tasks")
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        logging.error(f"User '{session['username']}' not found in the database")
        return jsonify({'message': 'User not found'}), 404

    try:
        if request.method == 'GET':
            tasks = Task.query.filter_by(user_id=user.id).all()
            logging.info(f"Tasks retrieved for user '{user.username}'")
            return jsonify([task.to_dictionary() for task in tasks])

        elif request.method == 'POST':
            data = request.get_json()
            if not data or 'task' not in data:
                logging.error("Invalid task data")
                return jsonify({'message': 'Invalid task data'}), 400

            new_task = Task(
                task=data['task'],
                description=data.get('description', ''),
                priority=data.get('priority', ''),
                status=data.get('status', True),
                task_date=data.get('task_date', ''),
                user_id=user.id
            )
            db.session.add(new_task)
            db.session.commit()
            logging.info(f"Task created for user '{user.username}'")
            return jsonify(new_task.to_dictionary()), 201

    except Exception as e:
        logging.error(f"Error getting task: {e}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    if 'username' not in session:
        logging.warning("Unauthorized")
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        logging.error(f"User '{session['username']}' not found in the database")
        return jsonify({'message': 'User not found'}), 404

    task = Task.query.filter_by(id=id, user_id=user.id).first()
    if not task:
        logging.warning(f"Task with id '{id}' not found for user '{user.username}'")
        return jsonify({'message': 'Task not found'}), 404

    try:
        if request.method == 'PUT':
            data = request.get_json()
            if not data:
                logging.error("Invalid update task data")
                return jsonify({'message': 'Invalid update data'}), 400

            task.task = data.get('task', task.task)
            task.description = data.get('description', task.description)
            task.priority = data.get('priority', task.priority)
            task.status = data.get('status', task.status)
            task.task_date = data.get('task_date', task.task_date)
            db.session.commit()
            logging.info(f"Task '{id}' updated for user '{user.username}'")
            return jsonify(task.to_dictionary())

        elif request.method == 'DELETE':
            db.session.delete(task)
            db.session.commit()
            logging.info(f"Task '{id}' deleted for user '{user.username}'")
            return '', 204

    except Exception as e:
        logging.error(f"Error in task modification: {e}")
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500



# Create Tables (run once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)  

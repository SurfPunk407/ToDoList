from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Sample data for tasks
tasks = [
    {"id": 1, "task": "Finish project", "description": "Complete the coding assignment", "status": "incomplete", "date": "2025-02-10"},
    {"id": 2, "task": "Buy groceries", "description": "Get milk and eggs", "status": "incomplete", "date": "2025-02-11"}
]

# Get all tasks (GET /tasks)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Fetch tasks for today or tomorrow
    date_filter = request.args.get('date')
    if date_filter:
        filtered_tasks = [task for task in tasks if task["date"] == date_filter]
        return jsonify(filtered_tasks)
    return jsonify(tasks)

# Add a new task (POST /tasks)
@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    new_task["id"] = len(tasks) + 1  # Assign an ID based on the current length
    tasks.append(new_task)
    return jsonify(new_task), 201

# Update task (PUT /tasks/<task_id>)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task.update(updated_task)
            return jsonify(task)
    return jsonify({"message": "Task not found"}), 404

# Delete a task (DELETE /tasks/<task_id>)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

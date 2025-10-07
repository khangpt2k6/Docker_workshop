from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage for tasks
tasks = {}
task_counter = 1

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Personal To-Do List API',
        'endpoints': {
            'GET /tasks': 'List all tasks',
            'GET /tasks/<id>': 'Get a specific task',
            'POST /tasks': 'Create a new task',
            'PUT /tasks/<id>': 'Update a task',
            'DELETE /tasks/<id>': 'Delete a task'
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({
        'success': True,
        'count': len(tasks),
        'tasks': list(tasks.values())
    })

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = tasks.get(task_id)
    if task:
        return jsonify({'success': True, 'task': task})
    return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    global task_counter
    
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'success': False, 'error': 'Title is required'}), 400
    
    task = {
        'id': task_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    tasks[task_counter] = task
    task_counter += 1
    
    return jsonify({'success': True, 'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify({'success': True, 'task': task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = tasks.pop(task_id, None)
    if task:
        return jsonify({'success': True, 'message': 'Task deleted', 'task': task})
    return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/taskdb')
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.taskdb
tasks_collection = db.tasks

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Task Manager API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'tasks': '/api/tasks'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for monitoring services"""
    try:
        client.admin.command('ping')
        db_status = 'connected'
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        db_status = f'disconnected: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'service': 'task-manager-api',
        'database': db_status
    }), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = list(tasks_collection.find())
        
        for task in tasks:
            task['_id'] = str(task['_id'])
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'count': len(tasks)
        }), 200
        
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': 'Database error occurred',
            'details': str(e)
        }), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    # Layer 1: Check Content-Type
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 415
    
    data = request.get_json()
    
    # Layer 2: Check required fields exist
    if not data or 'title' not in data:
        return jsonify({
            'success': False,
            'error': 'Title is required'
        }), 400
    
    # Layer 3: Check field is not empty
    if not data['title'].strip():
        return jsonify({
            'success': False,
            'error': 'Title cannot be empty'
        }), 400
    
    # Layer 4: Database operation with error handling
    try:
        task = {
            'title': data['title'].strip(),
            'description': data.get('description', '').strip(),
            'completed': bool(data.get('completed', False)),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'task': task
        }), 201
        
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': 'Failed to create task',
            'details': str(e)
        }), 500
        
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    # Validate ObjectId format FIRST
    try:
        obj_id = ObjectId(task_id)
    except InvalidId:
        return jsonify({
            'success': False,
            'error': 'Invalid task ID format'
        }), 400
    
    # Then query database
    try:
        task = tasks_collection.find_one({'_id': obj_id})
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        task['_id'] = str(task['_id'])
        return jsonify({
            'success': True,
            'task': task
        }), 200
        
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve task',
            'details': str(e)
        }), 500
        
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    # Step 1: Validate ObjectId
    try:
        obj_id = ObjectId(task_id)
    except InvalidId:
        return jsonify({'error': 'Invalid task ID format'}), 400
    
    # Step 2: Validate Content-Type
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.get_json()
    
    # Step 3: Check data exists
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Step 4: Build update fields with validation
    update_fields = {}
    
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        update_fields['title'] = data['title'].strip()
    
    if 'description' in data:
        update_fields['description'] = data['description'].strip()
    
    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return jsonify({'error': 'Completed must be a boolean'}), 400
        update_fields['completed'] = data['completed']
    
    # Step 5: Ensure at least one field to update
    if not update_fields:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    update_fields['updated_at'] = datetime.utcnow()
    
    # Step 6: Database operation
    try:
        result = tasks_collection.update_one(
            {'_id': obj_id},
            {'$set': update_fields}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Task updated successfully'
        }), 200
        
    except PyMongoError as e:
        return jsonify({'error': 'Failed to update task'}), 500
    
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    # Validate ObjectId format
    try:
        obj_id = ObjectId(task_id)
    except InvalidId:
        return jsonify({'error': 'Invalid task ID format'}), 400
    
    try:
        result = tasks_collection.delete_one({'_id': obj_id})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
        
    except PyMongoError as e:
        return jsonify({'error': 'Failed to delete task'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


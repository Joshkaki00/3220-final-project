from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/taskdb')
client = MongoClient(MONGO_URI)
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
    return jsonify({
        'status': 'healthy',
        'service': 'task-manager-api',
        'database': 'connected'
    }), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks - placeholder for implementation"""
    return jsonify({
        'tasks': [],
        'message': 'Task retrieval endpoint - to be implemented'
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task - placeholder for implementation"""
    return jsonify({
        'message': 'Task creation endpoint - to be implemented'
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


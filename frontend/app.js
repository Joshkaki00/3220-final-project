// API Configuration
const API_URL = '/api';
const HEALTH_URL = '/health';

// Check health on page load
checkHealth();
loadTasks();

// Health check function
function checkHealth() {
    fetch(HEALTH_URL)
        .then(response => response.json())
        .then(data => {
            const statusEl = document.getElementById('health-status');
            if (data.status === 'healthy' && data.database === 'connected') {
                statusEl.textContent = 'Status: Connected to backend';
            } else {
                statusEl.textContent = 'Status: Backend issues detected';
            }
        })
        .catch(error => {
            document.getElementById('health-status').textContent = 'Status: Cannot connect to backend';
            console.error('Health check failed:', error);
        });
}

// Load and display tasks
function loadTasks() {
    fetch(`${API_URL}/tasks`)
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('task-list');
            
            if (data.success && data.tasks && data.tasks.length > 0) {
                taskList.innerHTML = '';
                data.tasks.forEach(task => {
                    const li = document.createElement('li');
                    li.textContent = task.title;
                    if (task.completed) {
                        li.textContent += ' (completed)';
                    }
                    taskList.appendChild(li);
                });
            } else {
                taskList.innerHTML = '<li>No tasks found</li>';
            }
        })
        .catch(error => {
            document.getElementById('task-list').innerHTML = '<li>Error loading tasks</li>';
            console.error('Failed to load tasks:', error);
        });
}

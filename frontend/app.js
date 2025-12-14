// API Configuration
const API_URL = '/api';
const HEALTH_URL = '/health';

// DOM Elements
let taskForm;
let taskInput;
let taskList;
let healthStatus;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    taskForm = document.getElementById('task-form');
    taskInput = document.getElementById('task-input');
    taskList = document.getElementById('task-list');
    healthStatus = document.getElementById('health-status');
    
    // Set up event listeners
    if (taskForm) {
        taskForm.addEventListener('submit', handleTaskSubmit);
    }
    
    // Check health status
    checkHealth();
    
    // Load tasks (placeholder)
    loadTasks();
});

// Health check function
async function checkHealth() {
    try {
        const response = await fetch(HEALTH_URL);
        const data = await response.json();
        
        if (response.ok && data.status === 'healthy') {
            healthStatus.textContent = '✅ Connected to backend';
            healthStatus.style.color = '#50c878';
        } else {
            healthStatus.textContent = '⚠️ Backend issues detected';
            healthStatus.style.color = '#e67e22';
        }
    } catch (error) {
        healthStatus.textContent = '❌ Cannot connect to backend';
        healthStatus.style.color = '#e74c3c';
        console.error('Health check failed:', error);
    }
}

// Handle task form submission
function handleTaskSubmit(event) {
    event.preventDefault();
    
    const taskText = taskInput.value.trim();
    if (!taskText) return;
    
    // Placeholder: Will implement API call later
    console.log('Task to create:', taskText);
    
    // Clear input
    taskInput.value = '';
    
    // Show temporary message
    alert('Task creation will be implemented in the next phase!');
}

// Load tasks from API
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const data = await response.json();
        
        console.log('Tasks loaded:', data);
        // Rendering logic will be implemented later
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

// Placeholder functions for future implementation
function createTask(taskData) {
    // TODO: Implement task creation
}

function updateTask(taskId, updates) {
    // TODO: Implement task update
}

function deleteTask(taskId) {
    // TODO: Implement task deletion
}

function renderTasks(tasks) {
    // TODO: Implement task rendering
}


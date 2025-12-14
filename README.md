# Task Manager Application

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Uptime](https://img.shields.io/badge/uptime-monitoring-success)

A modern, containerized task management web application built with Flask, MongoDB, and Docker.

## 🚀 Features

- RESTful API backend with Flask
- MongoDB database for data persistence
- Modern responsive frontend interface
- Multi-container Docker setup
- Health check monitoring
- Production-ready deployment

## 🛠 Tech Stack

- **Backend**: Python 3.11, Flask, Gunicorn
- **Database**: MongoDB 6.0
- **Frontend**: HTML5, CSS3, JavaScript, Nginx
- **DevOps**: Docker, Docker Compose

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## 🏗 Building the Application

Clone the repository and build the containers:

```bash
# Clone the repository
git clone <your-repo-url>
cd 3220-final-project

# Build all containers
docker-compose build
```

## ▶️ Running the Application

Start all services with Docker Compose:

```bash
# Start in foreground
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🏥 Health Monitoring

The application includes a `/health` endpoint that can be monitored by services like FreshPing:

```bash
curl http://localhost:5000/health
```

## 📦 Services

The application consists of three Docker containers:

1. **MongoDB** (port 27017) - Database service
2. **Flask Backend** (port 5000) - REST API
3. **Nginx Frontend** (port 80) - Web interface

## 🚀 Deployment

This application is configured for deployment on CapRover:

1. Initialize your CapRover app
2. Push the repository to CapRover
3. The `captain-definition` file will handle the deployment

### Environment Variables

Configure these environment variables in your deployment:

- `MONGO_URI` - MongoDB connection string (default: mongodb://mongodb:27017/taskdb)
- `FLASK_ENV` - Flask environment (production/development)

## 📝 API Documentation

### Endpoints

- `GET /health` - Health check endpoint
- Additional endpoints to be documented as implemented

## 🔧 Development

For local development without Docker:

```bash
# Backend
cd app
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
# Serve with any static file server
```

## 📄 License

This project is created for educational purposes as part of a DevOps course final project.

## 👤 Author

Joshua Kakinuki

## 🙏 Acknowledgments

- Course: Make School DevOps
- Instructor: [Instructor Name]


# Spanish Language Learning Portal

A web application for learning Spanish vocabulary and tracking your progress.

## Features
- Spanish vocabulary organized into logical groups
- Interactive learning activities
- Progress tracking
- Pronunciation guides for Spanish words

## Project Structure
- `backend_flask/` - Python Flask backend API
- `frontend-react/` - React frontend application

## Backend Setup

### Install Dependencies

```sh
cd backend_flask
uv pip install -r requirements.txt
```

Or using standard pip:
```sh
cd backend_flask
pip install -r requirements.txt
```

### Initialize Database

```sh
cd backend_flask
uv run -m invoke init-db
```

### Run Backend Server

```sh
cd backend_flask
uv run app.py
```

The backend API will start on http://localhost:5000

## Frontend Setup

### Install Dependencies

```sh
cd frontend-react
npm install
```

### Run Development Server

```sh
cd frontend-react
npm run dev
```

The frontend application will start on http://localhost:5173

## Production Build

```sh
cd frontend-react
npm run build
```

## Accessing the Application

Once both backend and frontend servers are running:
1. Backend API: http://localhost:5000
2. Frontend application: http://localhost:5173
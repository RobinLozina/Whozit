Whozit? - Multiplayer Game

Welcome to the Whozit? Multiplayer Game! This is an online version of the classic "Guess Who" game that allows two players to play against each other in real-time. The backend is powered by Django and Django Channels for WebSockets, while the frontend uses Vue.js for a dynamic and interactive experience.

Table of Contents

Project Overview

Features

Technology Stack

Prerequisites

Installation

Running the Application Locally

Deploying to Production

Usage

Folder Structure

License

Project Overview

This project is an online version of "Guess Who" where players can create rooms, join rooms, and play against each other in real-time. The game utilizes Django for backend logic and API handling, and Vue.js for the front-end user interface. Real-time communication between players is handled using WebSockets via Django Channels, allowing for a smooth and interactive gaming experience.

Features

Real-time multiplayer gameplay.

Room creation and joining using unique room codes.

Dynamic game board with characters, allowing players to guess the opponent's character.

WebSocket implementation for real-time communication.

Ability to customize characters by selecting folders with character sets.

Technology Stack

Backend: Django, Django Channels, WebSockets

Frontend: Vue.js, TailwindCSS

Database: SQLite (for development), PostgreSQL (recommended for production)

WebSockets: Channels with Redis (in production)

Prerequisites

Python 3.8+: Make sure Python is installed on your system.

Node.js and npm: To run the Vue.js frontend.

Redis (for production): Used for managing WebSocket connections.

Installation

Backend Setup

Clone the repository:

git clone https://github.com/RobinLozina/Whozit.git
cd guesswho

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`

Install the dependencies:

pip install -r requirements.txt

Run database migrations:

python manage.py migrate

Create a .env file for environment variables:

DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

Frontend Setup

Navigate to the frontend directory:

cd frontend

Install the dependencies:

npm install

Build the Vue.js frontend:

npm run build

The build output will be stored in the dist/ directory.

Running the Application Locally

Backend

Run the Django server:

python manage.py runserver

Run the Django Channels ASGI server (using Daphne or other ASGI server for WebSockets):

daphne -b 0.0.0.0 -p 8001 guesswho.asgi:application

Frontend

Start the Vue development server:

npm run serve

Access the application at http://localhost:8080.

Deploying to Production

Use a production-grade database like PostgreSQL.

Use Redis as the channel layer backend for handling WebSockets.

Serve the Django application using Daphne or Uvicorn.

Set up nginx as a reverse proxy for handling SSL certificates and serving static files.

Usage

Players can create a new room by clicking "Generate New Room".

Share the room link with another player to join.

Guess your opponent's character by selecting options from the game board.

The game will notify both players when someone wins or loses.

Folder Structure

guesswho/
|-- guessWho/ # Main Django project folder
|-- gameLogic/ # Application logic and models
|-- templates/ # Django HTML templates
|-- static/ # Static files (images, CSS, JavaScript)
|-- media/ # Media files (uploaded character images)
|-- frontend/ # Vue.js front-end application
|-- requirements.txt # Python dependencies
|-- README.md # Project documentation

License

This project is licensed under the MIT License. See the LICENSE file for more details.

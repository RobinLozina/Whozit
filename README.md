# Whozit? - Multiplayer Game

Welcome to the **Whozit?** Multiplayer Game! This is an online version of the classic "Guess Who" game that allows two players to play against each other in real-time. The backend is powered by **Django** and **Django Channels** for WebSockets, while the frontend uses **Vue.js** for a dynamic and interactive experience.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Running the Application Locally](#running)
5. [License](#license)

## Project Overview

This project is an online version of "Guess Who" where players can create rooms, join rooms, and play against each other in real-time. The game utilizes **Django** for backend logic and API handling, and **Vue.js** for the front-end user interface. Real-time communication between players is handled using **WebSockets** via Django Channels, allowing for a smooth and interactive gaming experience.

## Features

- Real-time multiplayer gameplay.
- Room creation and joining using unique room codes.
- Dynamic game board with characters, allowing players to guess the opponent's character.
- WebSocket implementation for real-time communication.
- Ability to customize characters by selecting folders with character sets.

## Technology Stack

- **Backend**: Django, Django Channels, WebSockets
- **Frontend**: Vue.js, TailwindCSS
- **Database**: SQLite (for development), PostgreSQL (recommended for production)
- **WebSockets**: Channels with Redis (in production)

## Running the Application Locally

1. **Clone the repository**:

   ```sh
   git clone https://github.com/RobinLozina/Whozit.git
   cd Whozit

   ```

2. **Create a virtual environment and activate it**:

   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

   ```

3. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt

   ```

4. **Run database migrations**:

   ```sh
   python manage.py migrate

   ```

5. **Run the ASGI server**:

   ```sh
   uvicorn guessWho.asgi:application --host 127.0.0.1 --port 8000

   ```

6. **Navigate to the frontend directory**:

   ```sh
   cd frontend/guesswho-client

   ```

7. **Install the dependencies**:

   ```sh
   npm install

   ```

8. **Start the Vue development server**:

   ```sh
   npm run serve
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

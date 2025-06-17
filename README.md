# Superheroes API

A Flask API for tracking heroes and their superpowers.

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
5. Seed the database:
   ```bash
   python seed.py
   ```
6. Run the application:
   ```bash
   python app.py

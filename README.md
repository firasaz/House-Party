# House Party Application
Create a room and play music with all of your friends in one space.

## Description
Web application utilizing Django and ReactJS where users authenticate with Spotify and play music with their friends. One member will create the room and be the host of the room. The host have full control over the room and can update settings of the room at any time. Up to 10 friends can join a single room where they can vote to skip a song and play/pause it. Host should have a premium spotify account for full functionalities to work but it is not a requirement.

## Prerequisites:
- Spotify account (preferably premium account).
- Python installed on your computer.
- Pip package manager
- Pipenv or venv to create your virtual environment (pipenv preferred)

## Installation:
1. Clone the repo to your local machine
2. Create virtual environment
3. cd into the cloned repo then run pipenv install -r requirements
4. All dependencies should be installed now. Run pipenv shell in the root directory, where Pipfile and Pipfile.lock files should be located.
5. Now that you entered the virtual environment, cd into src folder and run this command: python manage.py runserver.
6. Congrats, you're done! Open your favorite browser and go to http://127.0.0.1:8000

## Steps:
### Clone Repo:
```
git clone https://github.com/firasaz/House-Party.git
cd House-Party
```
### Create Virtual Environment:
- **Python Venv Module:**
Run these commands in the root folder of the project.
```
# Create virtual environment
python -m venv venv
# Activate created virtual environment
./venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```
- **Pipenv Virtual Environment:**
```
# Install pipenv
pip install pipenv
```
```
# Create and run virtual environment with dependencies
pipenv install -r requirements.txt
pipenv shell
```
### Run Server
```
cd src
python manage.py runserver
```
### Open Web Application
Congrats, you're done! Open your favorite browser and go to http://127.0.0.1:8000

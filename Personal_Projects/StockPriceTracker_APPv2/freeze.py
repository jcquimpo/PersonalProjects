from flask_frozen import Freezer
# Replace 'app' with the name of your python file if it isn't app.py
# e.g., from main import app
from app import app 

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
from app import app  # Import the app instance directly
from extensions import db
from models import User, Password  # Import your models

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()

# from app import app, db  # Replace 'your_application' with the name of your main app file (without .py)

# with app.app_context():
#     db.create_all()  # This creates all tables defined in your models
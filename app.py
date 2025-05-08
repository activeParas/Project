from flask import Flask, redirect, url_for
from extensions import db, bcrypt, login_manager
from config import Config
from models import User, Password
from auth import auth as auth_blueprint
from views import views as views_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(views_blueprint)

# Create the database tables
with app.app_context():
    db.create_all()

# Define a route for the root URL
@app.route('/')
def home():
    return redirect(url_for('auth.login'))  # Redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)

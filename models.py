from extensions import db, bcrypt
from flask_login import UserMixin
from cryptography.fernet import Fernet
import hashlib

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    encrypted_password = db.Column(db.LargeBinary, nullable=False)  # Store encrypted password as binary
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='passwords')

    # Hardcoded encryption key (must be 32 bytes for AES-256)
    ENCRYPTION_KEY = b'KHp3NWM39XEoAjXz-A9bCj0HD6YQ93j8X9WjxqD2Xgw='  # Replace with your actual key

    def encrypt_password(self, password):
        """Encrypt the password using AES-256."""
        fernet = Fernet(self.ENCRYPTION_KEY)
        return fernet.encrypt(password.encode())

    def decrypt_password(self):
        """Decrypt the password using AES-256."""
        fernet = Fernet(self.ENCRYPTION_KEY)
        return fernet.decrypt(self.encrypted_password).decode()
    
    def __repr__(self):
        return f"<Password {self.name}>"
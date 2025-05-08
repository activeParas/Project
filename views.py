from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Password
from extensions import db
from cryptography.fernet import Fernet

views = Blueprint('views', __name__)

@views.route('/dashboard')
@login_required
def dashboard():
    passwords = Password.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', passwords=passwords)

@views.route('/add_password', methods=['POST'])
@login_required
def add_password():
    website = request.form.get('website')
    email = request.form.get('email')
    password = request.form.get('password')
    notes = request.form.get('notes', '')

    # Validate required fields
    if not website or not email or not password:
        flash('Please fill in all required fields: Website, Email, and Password.', 'danger')
        return redirect(url_for('views.dashboard'))

    # Encrypt the password
    new_password = Password(
        name=website,
        email=email,
        encrypted_password=Password().encrypt_password(password),  # Encrypt the password
        notes=notes,
        user_id=current_user.id
    )

    # Add to the database
    db.session.add(new_password)
    db.session.commit()

    flash('Password added successfully!', 'success')
    return redirect(url_for('views.dashboard'))

@views.route('/edit_password/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_password(id):
    password = Password.query.get_or_404(id)
    
    if request.method == 'POST':
        password.name = request.form.get('website')
        password.email = request.form.get('email')
        
        # Get the new password from the form
        new_password = request.form.get('password')
        
        # Check if the new password is provided
        if new_password:
            password.encrypted_password = Password().encrypt_password(new_password)  # Encrypt the new password
        else:
            # If no new password is provided, keep the existing encrypted password
            flash('No new password provided. Keeping the existing password.', 'warning')
        
        password.notes = request.form.get('notes', '')
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('views.dashboard'))
    
    return render_template('edit_password.html', password=password)

@views.route('/delete_password/<int:id>', methods=['GET'])
@login_required
def delete_password(id):
    password = Password.query.get_or_404(id)
    db.session.delete(password)
    db.session.commit()
    flash('Password deleted successfully!', 'success')
    return redirect(url_for('views.dashboard'))

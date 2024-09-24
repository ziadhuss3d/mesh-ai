import os
from flask import Flask, render_template, redirect, url_for, request, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, BlenderModel  # Import db and models

app = Flask(__name__)
app.config.from_object(Config)

# Configure upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = 'uploads'  # Change this to your desired upload directory
app.config['ALLOWED_EXTENSIONS'] = {'blend'}  # Adjust extensions as needed

db.init_app(app)  # Initialize SQLAlchemy

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')  # Ensure this template exists

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        print(f"Email: {email}")
        print(f"user: {user}")
        if user is None or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('dashboard'))  # Ensure you have a dashboard route

    return render_template('login.html')  # Ensure this template exists

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)  # Pass current_user to the template

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Save the model information in the database
            new_model = BlenderModel(filename=filename, user_id=current_user.id)
            db.session.add(new_model)
            db.session.commit()
            
            flash('Model uploaded successfully!')
            return redirect(url_for('dashboard'))

    return render_template('upload.html')  # Ensure this template exists

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

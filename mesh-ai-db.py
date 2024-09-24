from app import app, db  # Import the app and db

# Create an application context
with app.app_context():
    db.create_all()  # Create the database and tables

print("Database and tables created successfully.")

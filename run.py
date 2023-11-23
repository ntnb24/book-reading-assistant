from app import app
from app.database import init_db

if __name__ == '__main__':
    print("Root path: ", app.root_path)
    # Initialize the database
    init_db()
    # Start the Flask application
    app.run(debug=True)
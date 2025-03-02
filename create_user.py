# filepath: /C:/Users/darob/Documents/Proyectos/apinz/web/api/create_user.py
from werkzeug.security import generate_password_hash
from models import db, User
from app import app

def create_user(username, password):
    with app.app_context():
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_user.py <username> <password>")
    else:
        create_user(sys.argv[1], sys.argv[2])
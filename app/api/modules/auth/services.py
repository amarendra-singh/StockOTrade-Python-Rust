from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.security import verify_password

def authenticate_user(
    db: Session,
    username: str = None,
    email: str = None,
    password: str = None,
):

    query = db.query(User)
    
    if username:
        user = query.filter(User.username == username).first()
    elif email:
        email = query.filter(User.email == email).first()
    else:
        return None

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user
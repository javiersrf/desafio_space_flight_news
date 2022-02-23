from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer,HTTPBasic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
seguranca_basic = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


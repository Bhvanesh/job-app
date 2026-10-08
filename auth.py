from datetime import datetime, timedelta
from jose import JWTError, jwt  # create and read JWT tokens
from passlib.context import CryptContext # hash the password

SECRET_KEY = "secret"
ALGORITHM = "HS256" #encrip method
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#hash password
def hash_password(password: str):
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#create token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#verify token
def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM] )
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
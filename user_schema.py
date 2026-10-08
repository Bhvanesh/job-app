from pydantic import BaseModel

class UserBase(BaseModel):
    username : str
    password : str
    nonhashed_password : str | None = None

class UserCreate(UserBase):
    pass

class userdetails(UserBase):
    id : int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str   # the JWT token string
    token_type: str  
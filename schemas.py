from pydantic import BaseModel

class Company_Info(BaseModel):
    CompanyName: str 
    Application: str | None = None
    Role: str | None = None
    Status: str
    Location: str | None = None

class Company_info_creat(Company_Info):
    pass

class Company_Details(Company_Info):
    id : int

    class Config:
        from_attributes = True
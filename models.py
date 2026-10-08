from sqlalchemy import Column, Integer, String, Boolean;
from database import Base;

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key = True, index = True )
    CompanyName = Column(String, nullable = False)
    Application = Column(String, nullable = True) 
    Role = Column(String, nullable = True)
    Status = Column(String, nullable = False)
    Location = Column(String, nullable = True)

    
from fastapi import FastAPI, HTTPException, Request;
from fastapi.responses import JSONResponse;
from schemas import Company_info_creat, Company_Details;
from models import Company;
from database import Base, engine, SessionLocal;
from fastapi import Depends;
from sqlalchemy.orm import Session;
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm;
from user_model import User;
from user_schema import UserBase, UserCreate, userdetails, Token;
from auth import create_access_token, verify_token, verify_password, hash_password; 
import time;
import logging;

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
Base.metadata.create_all(bind=engine)


app = FastAPI()

logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s", 
                    handlers = [
                        logging.StreamHandler(),
                        logging.FileHandler("app.log")
                    ]
                )
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_request(request: Request, call_next):

    start_time = time.time()
    logger.info(f"{request.method} is started at {start_time}")
    
    response = await call_next(request)
    end_time = time.time()
    logger.info(f"{request.method} is completed at {end_time}")
    
    total_time = (end_time - start_time)*1000
    logger.info(f"Time taken for {request.method} is {end_time}")   
    
    print(f"Request:{request.method},{request.url}, Time taken: {total_time}ms")
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error | {request.method} {request.url} | {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )


def error_response(status_code: int, message: str):
    raise HTTPException(
        status_code=status_code,
        detail={"status": "error", "message": message}
    )

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
async def register_user(user : UserCreate, db : Session = Depends(get_db)):

    try:

        logger.info(f"Registering user: {user.username}")
        existing = db.query(User).filter(User.username == user.username).first()

        if existing:
            logger.warning(f"Username already exists: {user.username}")
            raise HTTPException(status_code=400, detail="Username already exists")

        Result = User(**user.dict())
        Result.nonhashed_password = Result.password
        Result.password = hash_password(Result.password)
        db.add(Result)
        db.commit()
        db.refresh(Result)
        logger.info(f"User registered successfully: {user.username}")
        return {"Message": "User registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error occured for {user.username}: {str(e)}")
        error_response(500, "Internal Server Error")

@app.post("/login")
async def login_user(userdetail : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    logger.info(f"Logging in user: {userdetail.username}")
    result = db.query(User).filter(User.username == userdetail.username).first()
    if not result or verify_password(userdetail.password, result.password) == False:
        logger.warning(f"Invalid login attempt for user: {userdetail.username}")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token(data={"sub": userdetail.username})
    logger.info(f"User logged in successfully: {userdetail.username}")
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    logger.info(f"Verifying token: {token}")
    username = verify_token(token)
    if not username:
        logger.warning(f"Invalid or expired token: {token}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"User not found for token: {token}")
        raise HTTPException(status_code=401, detail="User not found")
    return user


##application endpoints for company information##




@app.post("/company", response_model = Company_Details)
async def create_info(info : Company_info_creat, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Creating company information for: {info.CompanyName}")
    result = Company(**info.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    logger.info(f"Company information created successfully for: {info.CompanyName}")
    return result


@app.put("/company/{companyname}", response_model = Company_Details)
async def update_info(companyname : str, updated: Company_info_creat, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    result = db.query(Company).filter(Company.CompanyName == companyname).first()

    if not result:
        logger.warning(f"Company not found for update: {companyname}")
        raise HTTPException(status_code = 404, detail = f'CompanyName : {companyname} not available')
    
    else:
        logger.info(f"Updating company information for: {companyname}")
        result.Status = updated.Status

        db.commit()
        db.refresh(result)
        logger.info(f"Company information updated successfully for: {companyname}")
        return result

@app.get("/company", response_model = list[Company_Details])
async def get_all_companies( db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info("Fetching all company information")
    result = db.query(Company).all()#.filter(Company.CompanyName == companyname).first()
    return result


@app.get("/company/{companyname}", response_model = Company_Details)
async def get_company(companyname : str, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.query(Company).filter(Company.CompanyName == companyname).first()
    if not result:
        logger.warning(f"Company not found: {companyname}")
        raise HTTPException(status_code = 404, detail = f'CompanyName : {companyname} not available')
    return result


@app.delete("/company/{companyname}", response_model = Company_Details)
async def delete_company(companyname : str, db : Session =Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.query(Company).filter(Company.CompanyName == companyname).first()
    if not result:
        logger.warning(f"Company not found for deletion: {companyname}")
        raise HTTPException(status_code = 404, detail = f'CompanyName : {companyname} not available')
    logger.info(f"Deleting company information for: {companyname}")
    db.delete(result)
    db.commit()
    logger.info(f"Company information deleted successfully for: {companyname}")     
    return {"detail": f"deleted company: {companyname}"}
from fastapi import FastAPI
from sqlmodel import Session , select
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from models import  Answers, Users

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:3000",  # React development server
    "https://example.com",    # Production frontend
    "*"
] # Define allowed origins (domains that can access your API)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allow these origins
    allow_credentials=True,       # Allow cookies, authentication headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)



@app.get("/")
async def root():
    return {"message": "hi"}


@app.post("/answers")
async def create_answer(answer: Answers):
    with Session(engine) as session:
        session.add(answer)
        session.commit()
        session.refresh(answer)
        return {"Message": answer}

@app.get("/answers/{id}")
async def read_answer(id):
    with Session(engine) as session:
        print(id, '------------------------')
        ans = session.get(Answers, id)
        return {'message': ans}

@app.post("/register")
async def register_user(users: Users):
    with Session(engine) as session:
        hashed = hashlib.sha256(users.password.encode()).hexdigest()
        users.password =  hashed
        session.add(users)
        session.commit()
        session.refresh(users)
        return {"Message": "user registered"}



@app.post("/login")
async def login_user(users: Users):
    with Session(engine) as session:
        existing_user  = session.exec(select(Users).where(Users.user_name == users.user_name)).first()
        if not existing_user:
            return {'Message': 'User not Found'}
        input_hashed = hashlib.sha256(users.password.encode()).hexdigest()
        if existing_user.password == input_hashed:
            return {'Message': 'Login Success'}
        return {"Message": "Incorrect password. Send 500 to 09560635269 to reset your password!"}

@app.get("/login/{id}")
async def get_users(id):
    with Session(engine) as session:
        print(id, '------------------------')
        ans = session.get(Users, id)
        return {'message': ans}


    

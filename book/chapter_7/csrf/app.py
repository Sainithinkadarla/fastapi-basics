from fastapi import FastAPI, Depends, status, HTTPException, Form, Response
from fastapi.security import APIKeyCookie
from models import User as UserModel, AccessToken, datetime, timezone
from database import create_all_tables, get_db, AsyncSession
from authentication import authenticate, create_access_token
from contextlib import asynccontextmanager
from sqlalchemy import select, exc
from schemas import UserRead, UserCreate, UserUpdate
from password import get_passord_hash
from fastapi.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware


TOKEN_COOKIE_NAME = "token"
CSRF_TOKEN = "RANDOM_VALUE"

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:9000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],)

app.add_middleware(CSRFMiddleware,
                   secret = CSRF_TOKEN,
                   sensitive_cookies = {TOKEN_COOKIE_NAME},
                   cookie_domain = "localhost")

async def get_current_user(token: str = Depends(APIKeyCookie), 
                           session: AsyncSession = Depends(get_db)):
    query = select(AccessToken).where(AccessToken.token == token, 
                                            AccessToken.expiration_date >= datetime.now(tz=timezone.utc))
    result = await session.execute(query)
    access_token: AccessToken | None = result.scalar_one_or_none()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return access_token.user

@app.post("/register", status_code=status.HTTP_201_CREATED,
           response_model=UserRead)
async def create_user(user_create: UserCreate,
                      session: AsyncSession = Depends(get_db)):
    hashed_password = await get_passord_hash(user_create.password)
    user = UserModel(**user_create.model_dump(exclude={"password"}), password = hashed_password)

    try: 
        session.add(user)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already exists")
    return user

@app.post("/login")
async def login(response: Response,
                email: str = Form(...), 
                password: str = Form(...), 
                session: AsyncSession = Depends(get_db)):
    user = await authenticate(email, password, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = await create_access_token(user, session)

    response.set_cookie(TOKEN_COOKIE_NAME, token.token, max_age=token.max_age(), 
                        secure=False, httponly=True, samesite='lax')
    
@app.post("/me", response_model=UserRead)
async def update_email(user_update: UserUpdate,
                       user: UserModel = Depends(get_current_user),
                       session: AsyncSession = Depends(get_db)):
    update_fields = user_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    return user

@app.get("/me", response_model=UserRead)
async def get_me(user: UserModel = Depends(get_current_user)):
    return user

@app.get("/csrf")
async def csrf_token():
    return None
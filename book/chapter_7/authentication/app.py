from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from contextlib import asynccontextmanager
from database import create_all_tables, get_async_session, AsyncSession
from schemas import UserRead, UserCreate, User
from password import get_hash_passwd
from sqlalchemy import exc, select
from models import User as UserModel, AccessToken, datetime, timezone
from authentication import authenticate, create_access_token


async def lifespan(app:FastAPI):
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)


async def get_current_user(token = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
                           session: AsyncSession = Depends(get_async_session)):
    query = select(AccessToken).where(AccessToken.token == token, 
                                      AccessToken.expiration_date >= datetime.now(tz=timezone.utc))
    result = await session.execute(query)
    access_token : AccessToken | None = result.scalar_one_or_none()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return access_token.user

# Storing a user their password securely
@app.post("/register", response_model=UserRead, status_code = status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, 
                        database: AsyncSession = Depends(get_async_session)):
    hashed_password = await get_hash_passwd(user_create.password)
    user = UserModel(**user_create.model_dump(exclude={"password"}), passwd=hashed_password)

    try: 
        database.add(user)
        await database.commit()
    except exc.IntegrityError:
        await database.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already exists")
    return user

# Retreiving the user and generating the access token
@app.post("/token")
async def create_token(form: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), 
                       session: AsyncSession = Depends(get_async_session)):
    email = form.username
    password = form.password
    user = await authenticate(email, password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = await create_access_token(user, session)

    return {"access_token": access_token.token, "token_type": "Bearer"}

@app.get("/protected-route", response_model=UserRead)
async def protected_route(user: User = Depends(get_current_user)):
    return user
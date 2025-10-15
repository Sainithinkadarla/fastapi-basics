from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from database import create_all_tables, get_async_session, AsyncSession
from schemas import UserRead, UserCreate, User
from password import get_hash_passwd
from sqlalchemy import exc
from models import User as UserModel

async def lifespan(app:FastAPI):
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

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

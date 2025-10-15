from database import AsyncSession
from sqlalchemy import select
from models import User, AccessToken
from password import verify_password

async def authenticate(email: str, passwd: str, session: AsyncSession):
    query = select(User).where(User.email == email)
    result = await session.execute(query)

    user: User | None = result.scalar_one_or_none()

    if user is None:
        return None
    
    if not verify_password(passwd, user.passwd):
        return None
    
    return user

async def create_access_token(user: User, session: AsyncSession) -> AccessToken:
    access_token = AccessToken(user = user)
    session.add(access_token)
    await session.commit()
    return access_token
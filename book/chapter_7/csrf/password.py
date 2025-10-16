from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def get_passord_hash(passwd: str):
    return pwd_context.hash(passwd)

async def verify_password(passwd: str, hashed_passwd: str):
    return pwd_context.verify(passwd, hashed_passwd)
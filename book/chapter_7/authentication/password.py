from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def get_has_passwd(passwd: str) -> str:
    return pwd_context.hash(passwd)
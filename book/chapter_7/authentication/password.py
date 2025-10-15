from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

async def get_hash_passwd(passwd: str) -> str:
    return pwd_context.hash(passwd)

async def verify_password(plain_passwd: str, hashed_passwd: str) -> bool:
    return pwd_context.verify(plain_passwd, hashed_passwd)
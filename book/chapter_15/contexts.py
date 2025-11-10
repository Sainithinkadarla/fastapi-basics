from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(
    sys.stderr,  # Or a file
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | <blue>n={extra[n]}</blue>",
    level="DEBUG"
)

def is_even(n) -> bool:
    logger_context = logger.bind(n=n)
    logger_context.debug("Checking even or not")
    if not isinstance(n, int):
        logger_context.error("Not an integer")
        raise TypeError
    return n % 2 == 0

if __name__ == "__main__":
    is_even(2)
    is_even("Hello")

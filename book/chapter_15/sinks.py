from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="WARNING")
logger.add("file.log", level="DEBUG", rotation="1 min")
logger.info("Started processor")

def is_even(n) -> bool:
    logger.debug(f"Checking whether {n} is odd or not")
    if not isinstance(n, int):
        logger.warning(f"{n} is not an integer")
        logger.error(f"{n} is not an integer")
    return n % 2 == 0

if __name__ == "__main__":
    is_even(2)
    is_even("Hello")
from loguru import logger

def is_even(n) -> bool:
    logger.debug(f"Checking whether {n} is odd or not")
    if not isinstance(n, int):
        logger.error(f"{n} is not an integer")
    return n % 2 == 0

if __name__ == "__main__":
    is_even(2)
    is_even("Hello")
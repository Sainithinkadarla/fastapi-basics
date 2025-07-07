# import time
# def task(name):
#     time.sleep(3)

# start = time.perf_counter()

# task('a')
# task('b')

# end = time.perf_counter()

# print(f"Finished in {end-start:.2f} seconds")

import asyncio
import time

async def task(name):
    await asyncio.sleep(3)
    print(f"job {name} executing")

async def main():
    await asyncio.gather(task('a'), task("b"))
    # await task("a")
    # await task("b")

start = time.perf_counter()

asyncio.run(main())

end = time.perf_counter()

print(f"{end-start:.2f} Seconds")
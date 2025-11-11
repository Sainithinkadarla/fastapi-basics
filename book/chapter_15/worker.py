import dramatiq
import time

from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host="172.17.0.3")
dramatiq.set_broker(redis_broker)

@dramatiq.actor()
def addition(a, b):
    time.sleep(2)
    print(a+b)

if __name__ == "__main__":
    addition.send(3, 5)
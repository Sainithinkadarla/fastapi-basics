from prometheus_client import Counter
import dramatiq
from time import sleep 
from random import randint
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host="172.17.0.3")
dramatiq.set_broker(redis_broker)

DICE_COUNTER = Counter("app_dice_rolls_total", 
                       "Total number of dice rolls for a face", 
                       labelnames=["face"])

@dramatiq.actor()
def rolling_dice():
    face = randint(1, 6)
    sleep(2)
    DICE_COUNTER.labels(face).inc()
    print(face)

if __name__ == "__main__":
    rolling_dice.send()
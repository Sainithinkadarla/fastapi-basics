import uuid
from text_to_image import Text2Image
from dramatiq.middleware import Middleware
from dramatiq.brokers.redis import RedisBroker
import dramatiq

class Text2ImageMiddleware(Middleware):
    def __init__(self):
        super().__init__()
        self.text_to_image = Text2Image()
    
    def after_process_boot(self, broker):
        self.text_to_image.load_model()
        return super().after_process_boot(broker)

text_to_image_middleware = Text2ImageMiddleware()
redis_broker = RedisBroker(host = "172.17.0.3")
redis_broker.add_middleware(text_to_image_middleware)
dramatiq.set_broker(redis_broker)

@dramatiq.actor()
def text_to_image_task(prompt: str, 
                       negative_prompt: str | None = None,
                       steps: int = 50):
    image = text_to_image_middleware.text_to_image.generate(prompt=prompt, 
                                                            negative_prompt=negative_prompt, 
                                                            steps=steps)
    image.save(f"{uuid.uuid4()}.png")
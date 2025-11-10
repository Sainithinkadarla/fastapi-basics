import asyncio
import uuid
from sqlalchemy import select
from settings import settings
from database import session_maker
from storage import Storage
from models import GenereatedImages
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

def get_image(id: int):
    async def _get_image(id: int) -> GenereatedImages:
        async with session_maker() as session:
            query = select(GenereatedImages).where(GenereatedImages.id == id)
            result = await session.execute(query)
            image = result.scalar_one_or_none()

            if image is None:
                raise Exception("Image does not exist")
            
            return image
    return asyncio.run(_get_image(id))

def update_progress(image: GenereatedImages, step: int):
    async def _update_progress(image: GenereatedImages, step: int):
        async with session_maker() as session:
            image.progress = int((step/image.steps) * 100)
            session.add(image)
            await session.commit()
        
    return asyncio.run(_update_progress(image, step))

def update_filename(image: GenereatedImages, filename: str):
    async def _update_filename(image: GenereatedImages, filename: str):
        async with session_maker() as session:
            image.filename = filename
            session.add(image)
            await session.commit()

    return asyncio.run(_update_filename(image, filename))

@dramatiq.actor()
def text_to_image_task(image_id: int):
    image = get_image(image_id)

    def callback(step, _timestep, _tensor):
        update_progress(image, step)

    image_output = text_to_image_middleware.text_to_image.generate(
            prompt=image.prompt, 
            negative_prompt=image.negative_prompt, 
            steps=image.steps,
            callback = callback
    )
    filename = f"{uuid.uuid4()}.png"

    storage = Storage()
    storage.upload_image(image_output, filename, settings.storage_bucket)

    update_filename(image, filename)
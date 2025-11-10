from datetime import timedelta
import io
from PIL import Image
from minio import Minio
from settings import settings

class Storage:
	def __init__(self):
		self.client = Minio(
			endpoint=settings.storage_endpoint,
			access_key=settings.storage_access_key,
			secret_key=settings.storage_secret_key
		)

	def ensure_bucket(self, bucket_name: str):
		bucket_exists = self.client.bucket_exists(bucket_name=bucket_name)
		if not bucket_exists:
			self.client.make_bucket(bucket_name=bucket_name)
			
	def upload_image(self, image: Image, object_name: str, bucket_name: str):
		self.ensure_bucket(bucket_name)
		
		image_data = io.BytesIO()
		image.save(image_data, format="PNG")
		image.seek(0)
		image_data_length = len(image_data.getvalue())

		self.client.put_object(bucket_name, object_name, image_data, length=image_data_length, content_type="image/png")

	def get_presigned_url(self, bucket_name: str, object_name: str, *, expires: timedelta = timedelta(days=7)):
		return self.client.presigned_get_object(bucket_name, object_name, expires=expires)
	
	


		
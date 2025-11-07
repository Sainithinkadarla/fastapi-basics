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

from typing import IO
from datetime import timedelta
from io import BytesIO
from minio.error import S3Error
from app.core.minio import minio_client
from app.core.config import settings


class StorageService:
    def __init__(self):
        self.client = minio_client
        self.bucket = settings.MINIO_BUCKET

    def upload_file(self, file: bytes | IO, filename: str, content_type: str = "application/octet-stream") -> str:
        try:
            if isinstance(file, bytes):
                file_data = BytesIO(file)
                length = len(file)
            else:
                file_data = file
                length = -1

            self.client.put_object(
                bucket_name=self.bucket,
                object_name=filename,
                data=file_data,
                length=length,
                part_size=10 * 1024 * 1024,  # 10 MB
                content_type=content_type
            )
            return f"{self.bucket}/{filename}"
        except S3Error as e:
            raise RuntimeError(f"Error  in MinIO: {e}")

    def get_presigned_url(self, filename: str, expires: int = 3600) -> str:
        try:
            url = self.client.get_presigned_url(
                method="GET",
                bucket_name=self.bucket,
                object_name=filename,
                expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            raise RuntimeError(f"Error create URL : {e}")

    def delete_file(self, filename: str) -> bool:
        try:
            self.client.remove_object(self.bucket, filename)
            return True
        except S3Error as e:
            raise RuntimeError(f"Error delete in MinIO: {e}")
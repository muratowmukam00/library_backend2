from typing import IO
from datetime import timedelta
from minio.error import S3Error
from app.core.minio import minio_client
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.client = minio_client
        self.bucket = settings.MINIO_BUCKET

    def upload_file(self, file: IO, filename: str, content_type: str = "application/octet-stream") -> str:
        """
        Uploads a file to the MinIO bucket.
        :param file: file-like object to upload
        :param filename: name of the file in the bucket
        :param content_type: MIME type of the file
        :return: path to the file in the bucket
        """
        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=filename,
                data=file,
                length=-1,  # let MinIO automatically calculate the file length
                part_size=10*1024*1024,  # 10 MB
                content_type=content_type
            )
            return f"{self.bucket}/{filename}"
        except S3Error as e:
            raise RuntimeError(f"Error uploading file to MinIO: {e}")

    def get_presigned_url(self, filename: str, expires: int = 3600) -> str:
        """
        Generates a temporary presigned URL to download a file from MinIO.
        :param filename: name of the file in the bucket
        :param expires: URL expiration time in seconds
        :return: presigned URL
        """
        try:
            url = self.client.get_presigned_url(
                method="GET",
                bucket_name=self.bucket,
                object_name=filename,
                expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            raise RuntimeError(f"Error generating presigned URL: {e}")

    def delete_file(self, filename: str) -> bool:
        """
        Deletes a file from the MinIO bucket.
        :param filename: name of the file
        :return: True if the file was successfully deleted
        """
        try:
            self.client.remove_object(self.bucket, filename)
            return True
        except S3Error as e:
            raise RuntimeError(f"Error deleting file from MinIO: {e}")

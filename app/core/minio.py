from minio import Minio
from minio.error import S3Error
from app.core.config import settings

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)


try:
    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        minio_client.make_bucket(settings.MINIO_BUCKET)
        print(f"Bucket '{settings.MINIO_BUCKET}' создан успешно.")
    else:
        print(f"Bucket '{settings.MINIO_BUCKET}' уже существует.")
except S3Error as e:
    print(f"Ошибка при работе с MinIO: {e}")

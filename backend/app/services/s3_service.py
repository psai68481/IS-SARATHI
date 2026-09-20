import os
import shutil
import logging
from typing import Optional, BinaryIO
from app.core.config import settings

logger = logging.getLogger("is_sarathi.s3")

class StorageService:
    def __init__(self):
        self.s3_client = None
        self.use_local = settings.USE_LOCAL_STORAGE or not settings.AWS_ACCESS_KEY_ID

        if not self.use_local:
            try:
                import boto3
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
                logger.info(f"Connected to AWS S3 bucket: {settings.AWS_S3_BUCKET}")
            except Exception as e:
                logger.warning(f"AWS S3 initialization failed ({e}), defaulting to local storage.")
                self.use_local = True

        if self.use_local:
            os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
            logger.info(f"Local storage active at: {settings.LOCAL_STORAGE_DIR}")

    def upload_file(self, file_obj: BinaryIO, filename: str, content_type: str = "application/pdf") -> str:
        if not self.use_local and self.s3_client:
            try:
                s3_key = f"standards/{filename}"
                self.s3_client.upload_fileobj(
                    file_obj,
                    settings.AWS_S3_BUCKET,
                    s3_key,
                    ExtraArgs={'ContentType': content_type}
                )
                return f"s3://{settings.AWS_S3_BUCKET}/{s3_key}"
            except Exception as e:
                logger.error(f"S3 upload error: {e}, saving locally.")

        # Local storage fallback
        dest_path = os.path.join(settings.LOCAL_STORAGE_DIR, filename)
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file_obj, buffer)
        return f"local://{dest_path}"

    def get_download_url(self, file_key: str, expires_in: int = 3600) -> str:
        if not self.use_local and self.s3_client and file_key.startswith("s3://"):
            raw_key = file_key.replace(f"s3://{settings.AWS_S3_BUCKET}/", "")
            try:
                return self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': settings.AWS_S3_BUCKET, 'Key': raw_key},
                    ExpiresIn=expires_in
                )
            except Exception as e:
                logger.error(f"Failed to generate presigned S3 url: {e}")
        
        # Local download endpoint
        clean_name = os.path.basename(file_key)
        return f"/api/v1/standards/documents/{clean_name}"

storage_service = StorageService()

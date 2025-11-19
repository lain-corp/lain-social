"""Media hosting helper for uploading local images to public URLs.

Supports S3 and Imgur for platforms that require publicly accessible media URLs
like Instagram Graph API, Twilio WhatsApp, etc.
"""

import os
import logging
from pathlib import Path
from typing import Optional
import mimetypes

import requests

logger = logging.getLogger(__name__)


class MediaHostingError(Exception):
    """Base exception for media hosting operations."""
    pass


class S3MediaHost:
    """Upload images to AWS S3 and return public URLs."""
    
    def __init__(self):
        self.bucket = os.getenv('AWS_S3_BUCKET')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not all([self.bucket, self.access_key, self.secret_key]):
            raise MediaHostingError("Missing AWS S3 credentials: AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
        
        try:
            import boto3
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
        except ImportError:
            raise MediaHostingError("boto3 package required for S3 hosting. Install with: pip install boto3")

    def upload(self, image_path: Path) -> str:
        """Upload image to S3 and return public URL."""
        try:
            key = f"lain-social/{image_path.name}"
            
            # Upload with public-read ACL
            self.s3.upload_file(
                str(image_path),
                self.bucket,
                key,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            # Return public URL
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
            logger.info(f"Uploaded to S3: {url}")
            return url
            
        except Exception as e:
            raise MediaHostingError(f"S3 upload failed: {e}")


class ImgurMediaHost:
    """Upload images to Imgur and return public URLs."""
    
    def __init__(self):
        self.client_id = os.getenv('IMGUR_CLIENT_ID')
        if not self.client_id:
            raise MediaHostingError("Missing IMGUR_CLIENT_ID environment variable")
    
    def upload(self, image_path: Path) -> str:
        """Upload image to Imgur and return public URL."""
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                headers = {'Authorization': f'Client-ID {self.client_id}'}
                
                resp = requests.post(
                    'https://api.imgur.com/3/image',
                    headers=headers,
                    files=files,
                    timeout=60
                )
            
            if resp.status_code != 200:
                raise MediaHostingError(f"Imgur API returned {resp.status_code}: {resp.text}")
            
            data = resp.json()
            if not data.get('success'):
                raise MediaHostingError(f"Imgur upload failed: {data}")
            
            url = data['data']['link']
            logger.info(f"Uploaded to Imgur: {url}")
            return url
            
        except requests.RequestException as e:
            raise MediaHostingError(f"Imgur upload failed: {e}")


class MediaHostingManager:
    """Manages media hosting using configured provider."""
    
    def __init__(self):
        """Initialize with the configured hosting provider."""
        provider = os.getenv('MEDIA_HOSTING_PROVIDER', 'imgur').lower()
        
        if provider == 's3':
            self.host = S3MediaHost()
        elif provider == 'imgur':
            self.host = ImgurMediaHost()
        else:
            raise MediaHostingError(f"Unknown media hosting provider: {provider}. Use 's3' or 'imgur'")
        
        self.provider = provider
        logger.info(f"Media hosting initialized: {provider}")
    
    def upload_image(self, image_path: Path) -> str:
        """Upload image and return public URL."""
        if not image_path.exists():
            raise MediaHostingError(f"Image file not found: {image_path}")
        
        return self.host.upload(image_path)


def get_media_host() -> MediaHostingManager:
    """Get a configured media hosting manager."""
    return MediaHostingManager()
"""Instagram platform integration using Graph API container + publish flow.

Instagram Graph API requires publicly accessible media URLs. This implementation:
1. Uploads the local image to a hosting service (S3/Imgur) to get a public URL
2. Creates an Instagram media container with that URL
3. Publishes the container to make the post live

Environment variables:
- INSTAGRAM_BUSINESS_ACCOUNT_ID: Instagram Business/Creator account ID
- FB_PAGE_ACCESS_TOKEN: Page access token with Instagram permissions
- MEDIA_HOSTING_PROVIDER: 's3' or 'imgur' (default: 'imgur')

For S3: AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
For Imgur: IMGUR_CLIENT_ID
"""

import os
import logging
import time
from pathlib import Path
from typing import Optional

import requests
from media_hosting import get_media_host, MediaHostingError

logger = logging.getLogger(__name__)


class InstagramPoster:
    """Handler for posting images to Instagram via Graph API."""

    platform_name = "Instagram"

    def __init__(self):
        self.business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')
        
        if not self.business_account_id or not self.access_token:
            raise ValueError("Missing INSTAGRAM_BUSINESS_ACCOUNT_ID or FB_PAGE_ACCESS_TOKEN environment variables")
        
        self.graph_version = os.getenv('FB_GRAPH_VERSION', 'v17.0')
        self.base_url = f"https://graph.facebook.com/{self.graph_version}"
        
        # Initialize media hosting
        try:
            self.media_host = get_media_host()
        except MediaHostingError as e:
            raise ValueError(f"Media hosting setup failed: {e}")

    def _create_container(self, image_url: str, caption: str) -> Optional[str]:
        """Create an Instagram media container."""
        url = f"{self.base_url}/{self.business_account_id}/media"
        params = {
            'access_token': self.access_token,
            'image_url': image_url,
            'caption': caption
        }
        
        try:
            resp = requests.post(url, params=params, timeout=30)
            
            if resp.status_code not in (200, 201):
                logger.error(f"Instagram container creation failed {resp.status_code}: {resp.text}")
                return None
            
            data = resp.json()
            container_id = data.get('id')
            logger.info(f"Instagram container created: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"Error creating Instagram container: {e}")
            return None

    def _publish_container(self, container_id: str) -> bool:
        """Publish the Instagram media container."""
        url = f"{self.base_url}/{self.business_account_id}/media_publish"
        params = {
            'access_token': self.access_token,
            'creation_id': container_id
        }
        
        try:
            resp = requests.post(url, params=params, timeout=30)
            
            if resp.status_code in (200, 201):
                data = resp.json()
                post_id = data.get('id')
                logger.info(f"Instagram post published: {post_id}")
                return True
            else:
                logger.error(f"Instagram publish failed {resp.status_code}: {resp.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing Instagram container: {e}")
            return False

    def post(self, image_path: Path, text: str) -> bool:
        """Post image to Instagram using the container + publish flow."""
        try:
            # Step 1: Upload image to hosting service to get public URL
            logger.info(f"Uploading {image_path.name} to hosting service...")
            image_url = self.media_host.upload_image(image_path)
            
            # Step 2: Create Instagram container
            logger.info("Creating Instagram container...")
            container_id = self._create_container(image_url, text)
            if not container_id:
                return False
            
            # Step 3: Wait a moment for container processing
            time.sleep(2)
            
            # Step 4: Publish the container
            logger.info("Publishing Instagram container...")
            return self._publish_container(container_id)
            
        except MediaHostingError as e:
            logger.error(f"Media hosting error: {e}")
            return False
        except Exception as e:
            logger.error(f"Instagram posting error: {e}")
            return False
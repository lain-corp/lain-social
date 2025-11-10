"""Mastodon platform integration."""

import os
import logging
from pathlib import Path
from typing import Optional

from mastodon import Mastodon

logger = logging.getLogger(__name__)


class MastodonPoster:
    """Handler for posting to Mastodon."""

    platform_name = "Mastodon"

    def __init__(self):
        """Initialize Mastodon API client."""
        self.access_token = os.getenv('MASTODON_ACCESS_TOKEN')
        self.api_base_url = os.getenv('MASTODON_API_BASE_URL', 'https://mastodon.social')

        if not self.access_token:
            raise ValueError("Missing Mastodon access token")

        self.client = Mastodon(
            access_token=self.access_token,
            api_base_url=self.api_base_url
        )

    def post(self, image_path: Path, text: str) -> bool:
        """Post image with text to Mastodon.
        
        Args:
            image_path: Path to the image file
            text: Text content for the post
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Upload media
            media = self.client.media_post(
                str(image_path),
                description="Lain Iwakura"
            )
            
            # Create status with media
            self.client.status_post(
                text,
                media_ids=[media['id']]
            )
            
            logger.info("Successfully posted to Mastodon")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Mastodon: {e}")
            return False

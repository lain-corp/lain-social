"""Facebook platform integration for posting photos to a Facebook Page.

This posts photos to a Page using a Page access token. It uploads the
local image file directly to the Graph API endpoint.
"""

import os
import logging
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class FacebookPoster:
    """Handler for posting images to a Facebook Page via Graph API."""

    platform_name = "Facebook"

    def __init__(self):
        self.page_id = os.getenv('FB_PAGE_ID')
        self.page_access_token = os.getenv('FB_PAGE_ACCESS_TOKEN')

        if not self.page_id or not self.page_access_token:
            raise ValueError("Missing FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN environment variables")

        # Optionally allow specifying a Graph API version
        self.graph_version = os.getenv('FB_GRAPH_VERSION', 'v17.0')
        self.base_url = f"https://graph.facebook.com/{self.graph_version}"

    def post(self, image_path: Path, text: str) -> bool:
        """Upload a photo to the configured Facebook Page with a caption.

        Uses the Page's access token. The image is uploaded as multipart
        form data to the /{page_id}/photos endpoint.
        """
        try:
            url = f"{self.base_url}/{self.page_id}/photos"
            params = {'access_token': self.page_access_token}

            with open(image_path, 'rb') as img_file:
                files = {'source': (image_path.name, img_file)}
                data = {'caption': text}
                resp = requests.post(url, params=params, data=data, files=files, timeout=60)

            if resp.status_code in (200, 201):
                logger.info("Successfully posted photo to Facebook Page")
                return True
            else:
                logger.error(f"Facebook Graph API returned {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return False

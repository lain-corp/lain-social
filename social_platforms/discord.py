"""Discord platform integration via webhook."""

import os
import logging
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class DiscordPoster:
    """Handler for posting to Discord using an incoming webhook."""

    platform_name = "Discord"

    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not self.webhook_url:
            raise ValueError("Missing DISCORD_WEBHOOK_URL environment variable")

    def post(self, image_path: Path, text: str) -> bool:
        """Post an image and text to Discord via webhook.

        This uploads the image as a file and posts the message content.
        """
        try:
            with open(image_path, 'rb') as f:
                files = {'file': (image_path.name, f)}
                data = {'content': text}
                resp = requests.post(self.webhook_url, data=data, files=files, timeout=30)

            if resp.status_code in (200, 204):
                logger.info("Successfully posted to Discord")
                return True
            else:
                logger.error(f"Discord webhook returned {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting to Discord: {e}")
            return False

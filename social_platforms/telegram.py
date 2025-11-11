"""Telegram platform integration using Bot API via HTTPS requests.

This implementation uses simple HTTP requests (no extra dependency) to
send photos via a bot token and chat id.
"""

import os
import logging
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class TelegramPoster:
    """Handler for posting to Telegram via Bot API."""

    platform_name = "Telegram"

    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not self.token or not self.chat_id:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables")

        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def post(self, image_path: Path, text: str) -> bool:
        """Send a photo with caption to the configured chat id."""
        try:
            url = f"{self.base_url}/sendPhoto"
            with open(image_path, 'rb') as img_file:
                files = {'photo': (image_path.name, img_file)}
                data = {'chat_id': self.chat_id, 'caption': text}
                resp = requests.post(url, data=data, files=files, timeout=30)

            if resp.status_code == 200:
                logger.info("Successfully posted to Telegram")
                return True
            else:
                logger.error(f"Telegram API returned {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting to Telegram: {e}")
            return False

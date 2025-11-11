"""WhatsApp integration using WhatsApp Cloud API (preferred) or guidance for Twilio.

This module implements sending images via the WhatsApp Cloud API by:
  1. Uploading the media binary to /{phone_number_id}/media
  2. Sending a message referencing the media id to the recipient

Environment variables used:
  - WHATSAPP_PHONE_NUMBER_ID: your WhatsApp Business Cloud phone-number-id
  - WHATSAPP_ACCESS_TOKEN: bearer token for the WhatsApp Cloud API
  - WHATSAPP_TO: destination phone number in international format (e.g. +15551234567)

If you prefer Twilio's WhatsApp messaging API, you'll need a publicly
accessible media URL; see notes below.
"""

import os
import logging
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class WhatsAppPoster:
    platform_name = "WhatsApp"

    def __init__(self):
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.to = os.getenv('WHATSAPP_TO')

        if not (self.phone_number_id and self.access_token and self.to):
            raise ValueError("Missing WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN or WHATSAPP_TO environment variables")

        self.base_url = os.getenv('WHATSAPP_API_BASE_URL', 'https://graph.facebook.com')

    def _upload_media(self, image_path: Path) -> Optional[str]:
        url = f"{self.base_url}/v17.0/{self.phone_number_id}/media"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        try:
            with open(image_path, 'rb') as f:
                files = {'file': (image_path.name, f, 'application/octet-stream')}
                resp = requests.post(url, headers=headers, files=files, timeout=60)

            if resp.status_code not in (200, 201):
                logger.error(f"WhatsApp media upload failed {resp.status_code}: {resp.text}")
                return None

            data = resp.json()
            # response contains 'id' for the uploaded media
            return data.get('id')

        except Exception as e:
            logger.error(f"Error uploading media to WhatsApp: {e}")
            return None

    def _send_image_message(self, media_id: str, text: str) -> bool:
        url = f"{self.base_url}/v17.0/{self.phone_number_id}/messages"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'messaging_product': 'whatsapp',
            'to': self.to,
            'type': 'image',
            'image': {
                'id': media_id,
                'caption': text
            }
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code in (200, 201):
                logger.info("Successfully sent WhatsApp image message")
                return True
            else:
                logger.error(f"WhatsApp send message failed {resp.status_code}: {resp.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False

    def post(self, image_path: Path, text: str) -> bool:
        """Upload image and send it via WhatsApp Cloud API."""
        try:
            media_id = self._upload_media(image_path)
            if not media_id:
                return False

            return self._send_image_message(media_id, text)

        except Exception as e:
            logger.error(f"WhatsApp posting error: {e}")
            return False

    # Notes for Twilio fallback (manual):
    # Twilio requires a publicly accessible media URL. If you have a
    # MEDIA_HOSTING_URL base (e.g. S3 or Imgur) where you can upload
    # local images, you can use Twilio's API with basic auth to send a
    # WhatsApp message with media_url parameter.

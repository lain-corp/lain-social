"""Signal integration via signal-cli REST API (placeholder adapter).

This implementation attempts to send messages using a running
signal-cli-rest-api instance (https://github.com/bbernhard/signal-cli-rest-api).

Environment variables:
  - SIGNAL_CLI_REST_URL (default: http://localhost:8080)
  - SIGNAL_RECIPIENT (recipient phone number in international format, e.g. +15551234567)

If you don't run signal-cli-rest-api, this module will log helpful
instructions instead of sending.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class SignalPoster:
    platform_name = "Signal"

    def __init__(self):
        self.api_url = os.getenv('SIGNAL_CLI_REST_URL', 'http://localhost:8080')
        self.recipient = os.getenv('SIGNAL_RECIPIENT')
        if not self.recipient:
            raise ValueError("Missing SIGNAL_RECIPIENT environment variable (recipient phone number)")

    def post(self, image_path: Path, text: str) -> bool:
        """Attempt to send a message with attachment via signal-cli REST API.

        This posts multipart/form-data to /v1/messages or /v1/send depending
        on the deployed API. We try common endpoints and log helpful
        instructions if it fails.
        """
        # Try the common endpoint /v1/send
        endpoints = [
            '/v1/send',
            '/v1/messages'
        ]

        for ep in endpoints:
            url = self.api_url.rstrip('/') + ep
            try:
                with open(image_path, 'rb') as f:
                    files = {'attachment': (image_path.name, f, 'application/octet-stream')}
                    data = {'message': text, 'recipients': json.dumps([self.recipient])}
                    resp = requests.post(url, data=data, files=files, timeout=60)

                if resp.status_code in (200, 201):
                    logger.info(f"Successfully sent Signal message via {url}")
                    return True
                else:
                    logger.debug(f"Signal endpoint {url} returned {resp.status_code}: {resp.text}")

            except Exception as e:
                logger.debug(f"Signal endpoint {url} request error: {e}")

        logger.error("Failed to send Signal message. Is signal-cli-rest-api running and reachable? See README notes.")
        logger.info("Hints: run signal-cli-rest-api locally and set SIGNAL_CLI_REST_URL and SIGNAL_RECIPIENT environment variables.")
        return False

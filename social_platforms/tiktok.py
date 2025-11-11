"""TikTok placeholder integration.

TikTok's Content API requires a developer app and OAuth flows. This
module provides a clear placeholder with guidance. If you have a TikTok
Content API integration, replace this with a real implementation.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class TikTokPoster:
    platform_name = "TikTok"

    def __init__(self):
        # Intentionally lightweight; real integration requires app credentials and OAuth
        pass

    def post(self, image_path: Path, text: str) -> bool:
        logger.info(f"[TikTok placeholder] Would post {image_path.name} with caption: {text[:80]}")
        logger.info("To integrate TikTok: register a developer app, obtain OAuth credentials and use the TikTok Content API to upload media and create posts.")
        return False

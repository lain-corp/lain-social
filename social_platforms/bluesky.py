"""Bluesky placeholder integration.

Bluesky (AT Protocol) clients and SDKs are evolving; a production
integration requires using the atproto/bsky client libraries and handling
authentication. This placeholder logs the intended action and provides
notes for implementing a real adapter.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BlueskyPoster:
    platform_name = "Bluesky"

    def __init__(self):
        # Real integration should use an atproto client and app-specific auth
        pass

    def post(self, image_path: Path, text: str) -> bool:
        logger.info(f"[Bluesky placeholder] Would post {image_path.name} with text: {text[:80]}")
        logger.info("To integrate Bluesky: use an atproto client (bsky) and implement posting via the app.bsky.feed.post or media upload flow.")
        return False

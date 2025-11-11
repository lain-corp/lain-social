"""Placeholder adapters for platforms that require more setup.

These adapters don't perform real posts. They provide clear logging and
instructions for the platform-specific integration that needs to be added.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GenericPlaceholderPoster:
    """Generic placeholder for unsupported or unimplemented platforms.

    Use this when the platform requires OAuth flows, business APIs, or
    other non-trivial setup. The placeholder simply logs the intended
    action and returns False.
    """

    def __init__(self, platform_name: str, notes: str = ""):
        self.platform_name = platform_name
        self.notes = notes

    def post(self, image_path: Path, text: str) -> bool:
        logger.info(f"[Placeholder] Would post to {self.platform_name}: {image_path.name} - {text[:80]}")
        if self.notes:
            logger.info(f"Notes: {self.notes}")
        return False

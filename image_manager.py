"""Manages Lain Iwakura images for posting."""

import os
import random
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class ImageManager:
    """Manages and provides Lain Iwakura images."""

    def __init__(self):
        """Initialize the image manager."""
        self.image_dir = Path(os.getenv('IMAGE_DIR', './images'))
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        # Create image directory if it doesn't exist
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a placeholder if no images exist
        if not self._get_image_list():
            self._create_placeholder()

    def _get_image_list(self) -> List[Path]:
        """Get list of all valid image files.
        
        Returns:
            List of image file paths
        """
        images = []
        for ext in self.supported_formats:
            images.extend(self.image_dir.glob(f'*{ext}'))
        return images

    def get_random_image(self) -> Optional[Path]:
        """Get a random image from the collection.
        
        Returns:
            Path to a random image, or None if no images available
        """
        images = self._get_image_list()
        
        if not images:
            logger.warning("No images found in image directory")
            return None
        
        selected = random.choice(images)
        logger.info(f"Selected image: {selected.name}")
        return selected

    def _create_placeholder(self):
        """Create a placeholder image with instructions."""
        placeholder_path = self.image_dir / 'README.txt'
        
        content = """LAIN SOCIAL BOT - IMAGE DIRECTORY

Please add Lain Iwakura images to this directory.

Supported formats: .jpg, .jpeg, .png, .gif, .webp

Images will be randomly selected and posted to configured social media platforms.

You can:
1. Download images from the internet (respecting copyright)
2. Use AI image generators to create Lain-inspired artwork
3. Use screenshots from Serial Experiments Lain (for fair use/educational purposes)

Make sure to only include images you have the right to post publicly.
"""
        
        placeholder_path.write_text(content)
        logger.info(f"Created placeholder README at {placeholder_path}")

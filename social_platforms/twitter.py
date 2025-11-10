"""Twitter/X platform integration."""

import os
import logging
from pathlib import Path
from typing import Optional

import tweepy

logger = logging.getLogger(__name__)


class TwitterPoster:
    """Handler for posting to Twitter/X."""

    platform_name = "Twitter/X"

    def __init__(self):
        """Initialize Twitter API client."""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

        if not all([self.api_key, self.api_secret, self.access_token, 
                    self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials")

        # Initialize API v1.1 for media upload
        auth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )
        self.api_v1 = tweepy.API(auth)

        # Initialize API v2 for tweeting
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def post(self, image_path: Path, text: str) -> bool:
        """Post image with text to Twitter.
        
        Args:
            image_path: Path to the image file
            text: Text content for the tweet
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Upload media using API v1.1
            media = self.api_v1.media_upload(filename=str(image_path))
            
            # Create tweet with media using API v2
            self.client.create_tweet(
                text=text,
                media_ids=[media.media_id]
            )
            
            logger.info("Successfully posted to Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return False

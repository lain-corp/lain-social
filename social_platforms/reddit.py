"""Reddit platform integration."""

import os
import logging
from pathlib import Path
from typing import Optional

import praw

logger = logging.getLogger(__name__)


class RedditPoster:
    """Handler for posting to Reddit."""

    platform_name = "Reddit"

    def __init__(self):
        """Initialize Reddit API client."""
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.username = os.getenv('REDDIT_USERNAME')
        self.password = os.getenv('REDDIT_PASSWORD')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'LainSocialBot/1.0')
        self.subreddit_name = os.getenv('REDDIT_SUBREDDIT', 'test')

        if not all([self.client_id, self.client_secret, self.username, self.password]):
            raise ValueError("Missing Reddit API credentials")

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent=self.user_agent
        )

    def post(self, image_path: Path, text: str) -> bool:
        """Post image with text to Reddit.
        
        Args:
            image_path: Path to the image file
            text: Text content for the post title
            
        Returns:
            True if successful, False otherwise
        """
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            
            # Submit image post
            subreddit.submit_image(
                title=text[:300],  # Reddit has a 300 character limit for titles
                image_path=str(image_path)
            )
            
            logger.info(f"Successfully posted to Reddit (r/{self.subreddit_name})")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Reddit: {e}")
            return False

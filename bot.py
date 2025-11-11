#!/usr/bin/env python3
"""
Lain Social Media Bot - Posts Lain Iwakura images with AI-generated comments
across multiple social media platforms.
"""

import os
import random
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import schedule
from dotenv import load_dotenv

from social_platforms.twitter import TwitterPoster
from social_platforms.reddit import RedditPoster
from social_platforms.discord import DiscordPoster
from social_platforms.telegram import TelegramPoster
from social_platforms.placeholder import GenericPlaceholderPoster
from social_platforms.facebook import FacebookPoster
from social_platforms.linkedin import LinkedInPoster
from social_platforms.tiktok import TikTokPoster
from social_platforms.bluesky import BlueskyPoster
from social_platforms.whatsapp import WhatsAppPoster
from social_platforms.signal import SignalPoster
from ai_comment_generator import CommentGenerator
from image_manager import ImageManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LainSocialBot:
    """Main bot class that coordinates posting across multiple platforms."""

    def __init__(self):
        """Initialize the bot with configuration from environment variables."""
        load_dotenv()
        
        self.image_manager = ImageManager()
        self.comment_generator = CommentGenerator()
        
        # Initialize platform posters based on available credentials
        self.posters = []
        
        if os.getenv('TWITTER_API_KEY'):
            try:
                self.posters.append(TwitterPoster())
                logger.info("Twitter poster initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Twitter poster: {e}")

        if os.getenv('REDDIT_CLIENT_ID'):
            try:
                self.posters.append(RedditPoster())
                logger.info("Reddit poster initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Reddit poster: {e}")

        # Discord (via webhook)
        if os.getenv('DISCORD_WEBHOOK_URL'):
            try:
                self.posters.append(DiscordPoster())
                logger.info("Discord poster initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Discord poster: {e}")

        # Telegram (via bot token)
        if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'):
            try:
                self.posters.append(TelegramPoster())
                logger.info("Telegram poster initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram poster: {e}")

            # Facebook Page photo upload
            if os.getenv('FB_PAGE_ID') and os.getenv('FB_PAGE_ACCESS_TOKEN'):
                try:
                    self.posters.append(FacebookPoster())
                    logger.info("Facebook poster initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize Facebook poster: {e}")

            # LinkedIn (UGC image posting)
            if os.getenv('LINKEDIN_ACCESS_TOKEN') and os.getenv('LINKEDIN_OWNER_URN'):
                try:
                    self.posters.append(LinkedInPoster())
                    logger.info("LinkedIn poster initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize LinkedIn poster: {e}")

            # WhatsApp (Cloud API)
            if os.getenv('WHATSAPP_PHONE_NUMBER_ID') and os.getenv('WHATSAPP_ACCESS_TOKEN') and os.getenv('WHATSAPP_TO'):
                try:
                    self.posters.append(WhatsAppPoster())
                    logger.info("WhatsApp poster initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize WhatsApp poster: {e}")

            # Signal via signal-cli REST API
            if os.getenv('SIGNAL_RECIPIENT'):
                try:
                    self.posters.append(SignalPoster())
                    logger.info("Signal poster initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize Signal poster: {e}")

        # Optional placeholders for other platforms (enable with ENABLE_PLACEHOLDERS=true)
        if os.getenv('ENABLE_PLACEHOLDERS', 'false').lower() == 'true':
            other_platforms = [
                ('Facebook', 'Use Meta Graph API / Instagram Graph API with appropriate app and permissions'),
                ('Instagram', 'Use Instagram Graph API (business account) or direct upload via Facebook Graph API'),
                ('Threads', 'Threads API is currently restricted; consider using Instagram Graph APIs if/when available'),
                ('Bluesky', 'Bluesky currently has a developer API; implement an ActivityPub or Bluesky client'),
                ('TikTok', 'TikTok API requires a developer account; consider using their Business API'),
                ('LinkedIn', 'Use LinkedIn Marketing APIs or REST endpoints with OAuth2'),
                ('YouTube', 'Use Google APIs (youtube.upload) with OAuth2 credentials'),
                ('Signal', 'Consider signal-cli or third-party gateways'),
                ('WhatsApp', 'Use WhatsApp Business API or Twilio WhatsApp integration')
            ]

            for name, note in other_platforms:
                self.posters.append(GenericPlaceholderPoster(name, notes=note))
                logger.info(f"Placeholder poster added for {name}")
        
        if not self.posters:
            logger.warning("No social media platforms configured!")
        
        # Configuration
        self.post_interval = int(os.getenv('POST_INTERVAL_HOURS', '6'))
        self.simultaneous_post = os.getenv('SIMULTANEOUS_POST', 'true').lower() == 'true'

    def generate_post(self) -> tuple[Optional[Path], Optional[str]]:
        """Generate a post with image and comment.
        
        Returns:
            Tuple of (image_path, comment_text)
        """
        try:
            image_path = self.image_manager.get_random_image()
            if not image_path:
                logger.error("No image available")
                return None, None
            
            # Pass image path to comment generator for multimodal AI
            comment = self.comment_generator.generate_comment(image_path)
            logger.info(f"Generated comment: {comment}")
            
            return image_path, comment
        except Exception as e:
            logger.error(f"Error generating post: {e}")
            return None, None

    def post_to_all_platforms(self):
        """Post to all configured social media platforms."""
        logger.info("Starting post cycle...")
        
        image_path, comment = self.generate_post()
        if not image_path or not comment:
            logger.error("Failed to generate post content")
            return
        
        successful_posts = 0
        failed_posts = 0
        
        for poster in self.posters:
            try:
                logger.info(f"Posting to {poster.platform_name}...")
                poster.post(image_path, comment)
                successful_posts += 1
                logger.info(f"Successfully posted to {poster.platform_name}")
                
                # Add delay between platforms if not posting simultaneously
                if not self.simultaneous_post and poster != self.posters[-1]:
                    time.sleep(random.randint(30, 90))
                    
            except Exception as e:
                failed_posts += 1
                logger.error(f"Failed to post to {poster.platform_name}: {e}")
        
        logger.info(f"Post cycle complete. Success: {successful_posts}, Failed: {failed_posts}")

    def run_scheduled(self):
        """Run the bot on a schedule."""
        logger.info(f"Bot starting with {self.post_interval} hour interval")
        
        # Post immediately on startup
        self.post_to_all_platforms()
        
        # Schedule regular posts
        schedule.every(self.post_interval).hours.do(self.post_to_all_platforms)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run_once(self):
        """Run the bot once and exit."""
        logger.info("Running bot in one-shot mode")
        self.post_to_all_platforms()


def main():
    """Main entry point."""
    bot = LainSocialBot()
    
    run_mode = os.getenv('RUN_MODE', 'scheduled')
    
    if run_mode == 'once':
        bot.run_once()
    else:
        bot.run_scheduled()


if __name__ == '__main__':
    main()

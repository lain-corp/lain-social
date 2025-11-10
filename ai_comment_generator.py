"""AI-powered comment generator for social media posts."""

import os
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class CommentGenerator:
    """Generates AI-powered comments about Lain Iwakura."""

    def __init__(self):
        """Initialize the comment generator."""
        self.use_ai = os.getenv('USE_AI_COMMENTS', 'false').lower() == 'true'
        self.ai_provider = os.getenv('AI_PROVIDER', 'openai')  # openai or anthropic
        
        # Fallback comments if AI is not available
        self.fallback_comments = [
            "Present day, present time... 🌐 #LainIwakura #SerialExperimentsLain",
            "The Wired and the real world are not so different after all 💫 #Lain",
            "No matter where you are, everyone is connected 🔗 #SerialExperimentsLain",
            "You don't need to understand. You only need to believe. ✨ #Lain",
            "The border between the real and virtual is starting to blur 🌌 #LainIwakura",
            "I am everywhere and nowhere at once 👁️ #SerialExperimentsLain #Lain",
            "Close the world, open the nExt 🚪 #Lain #Cyberpunk",
            "God is here, in the Wired 🌐 #SerialExperimentsLain",
            "Are you enjoying the Wired? 💻 #LainIwakura #90sAnime",
            "Let's all love Lain 💙 #Lain #SerialExperimentsLain",
            "Reality is just another protocol 📡 #LainIwakura #Cyberpunk",
            "The network is vast and infinite 🌟 #SerialExperimentsLain #Lain",
            "I exist in the Wired and the real world simultaneously 🔀 #Lain",
            "Fulfilling the prophecy of the Wired 🎭 #LainIwakura #Anime",
            "Communication defines our existence 📱 #SerialExperimentsLain",
        ]
        
        if self.use_ai:
            self._init_ai_client()

    def _init_ai_client(self):
        """Initialize AI client based on provider."""
        try:
            if self.ai_provider == 'openai':
                import openai
                self.openai_client = openai.OpenAI(
                    api_key=os.getenv('OPENAI_API_KEY')
                )
            elif self.ai_provider == 'anthropic':
                import anthropic
                self.anthropic_client = anthropic.Anthropic(
                    api_key=os.getenv('ANTHROPIC_API_KEY')
                )
            logger.info(f"AI provider '{self.ai_provider}' initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize AI provider: {e}. Using fallback comments.")
            self.use_ai = False

    def generate_comment(self) -> str:
        """Generate a comment about Lain Iwakura.
        
        Returns:
            Generated comment text
        """
        if self.use_ai:
            try:
                return self._generate_ai_comment()
            except Exception as e:
                logger.error(f"Error generating AI comment: {e}")
                logger.info("Falling back to predefined comments")
        
        return self._generate_fallback_comment()

    def _generate_ai_comment(self) -> str:
        """Generate comment using AI.
        
        Returns:
            AI-generated comment
        """
        prompt = """Generate a short, engaging social media post (under 280 characters) about Lain Iwakura from Serial Experiments Lain. 
The post should be thoughtful, slightly mysterious, and relate to themes of technology, consciousness, or the internet.
Include 1-2 relevant hashtags. Use emojis sparingly but effectively."""

        if self.ai_provider == 'openai':
            response = self.openai_client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "You are a creative social media manager who loves Serial Experiments Lain."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.9
            )
            return response.choices[0].message.content.strip()
        
        elif self.ai_provider == 'anthropic':
            response = self.anthropic_client.messages.create(
                model=os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307'),
                max_tokens=100,
                temperature=0.9,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        
        return self._generate_fallback_comment()

    def _generate_fallback_comment(self) -> str:
        """Generate a comment from predefined list.
        
        Returns:
            Random predefined comment
        """
        return random.choice(self.fallback_comments)

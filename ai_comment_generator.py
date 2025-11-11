"""AI-powered comment generator for social media posts."""

import os
import random
import logging
import base64
from pathlib import Path
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class CommentGenerator:
    """Generates AI-powered comments about Lain Iwakura."""

    def __init__(self):
        """Initialize the comment generator."""
        self.use_ai = os.getenv('USE_AI_COMMENTS', 'false').lower() == 'true'
        self.ai_provider = os.getenv('AI_PROVIDER', 'openrouter')  # openai, anthropic, or openrouter
        
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
            elif self.ai_provider == 'openrouter':
                self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
                self.openrouter_model = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')
                if not self.openrouter_api_key:
                    raise ValueError("OPENROUTER_API_KEY is required for OpenRouter provider")
            logger.info(f"AI provider '{self.ai_provider}' initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize AI provider: {e}. Using fallback comments.")
            self.use_ai = False

    def generate_comment(self, image_path: Optional[Path] = None) -> str:
        """Generate a comment about Lain Iwakura.
        
        Args:
            image_path: Optional path to the image for multimodal generation
        
        Returns:
            Generated comment text
        """
        if self.use_ai:
            try:
                return self._generate_ai_comment(image_path)
            except Exception as e:
                logger.error(f"Error generating AI comment: {e}")
                logger.info("Falling back to predefined comments")
        
        return self._generate_fallback_comment()

    def _encode_image(self, image_path: Path) -> str:
        """Encode image to base64 string.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _get_image_mime_type(self, image_path: Path) -> str:
        """Get MIME type for image based on extension.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            MIME type string
        """
        extension = image_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(extension, 'image/jpeg')

    def _generate_ai_comment(self, image_path: Optional[Path] = None) -> str:
        """Generate comment using AI.
        
        Args:
            image_path: Optional path to the image for multimodal generation
        
        Returns:
            AI-generated comment
        """
        if self.ai_provider == 'openrouter' and image_path:
            return self._generate_openrouter_comment(image_path)
        
        # Fallback to text-only for other providers
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
    
    def _generate_openrouter_comment(self, image_path: Path) -> str:
        """Generate comment using OpenRouter API with image input.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            AI-generated comment based on the image
        """
        try:
            # Encode image to base64
            image_base64 = self._encode_image(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            # Prepare the multimodal request
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = """Analyze this image of Lain Iwakura from Serial Experiments Lain and generate a short, engaging social media post (under 280 characters).
The post should be thoughtful, slightly mysterious, and relate to what you see in the image as well as themes of technology, consciousness, or the internet.
Include 1-2 relevant hashtags. Use emojis sparingly but effectively."""
            
            payload = {
                "model": self.openrouter_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.9
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            comment = result['choices'][0]['message']['content'].strip()
            logger.info(f"Generated OpenRouter comment with image: {comment}")
            return comment
            
        except Exception as e:
            logger.error(f"Error generating OpenRouter comment: {e}")
            raise

    def _generate_fallback_comment(self) -> str:
        """Generate a comment from predefined list.
        
        Returns:
            Random predefined comment
        """
        return random.choice(self.fallback_comments)

#!/usr/bin/env python3
"""
Test script for OpenRouter multimodal AI comment generation.
This script demonstrates how the bot generates contextual comments based on images.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from ai_comment_generator import CommentGenerator
from image_manager import ImageManager

def test_openrouter():
    """Test OpenRouter image-based comment generation."""
    # Load environment variables
    load_dotenv()
    
    # Check if OpenRouter is configured
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY not set in environment")
        print("Please set the following in your .env file:")
        print("  USE_AI_COMMENTS=true")
        print("  AI_PROVIDER=openrouter")
        print("  OPENROUTER_API_KEY=your_key_here")
        print("  OPENROUTER_MODEL=anthropic/claude-3.5-sonnet")
        return
    
    # Verify AI is enabled
    if os.getenv('USE_AI_COMMENTS', 'false').lower() != 'true':
        print("❌ USE_AI_COMMENTS is not set to 'true'")
        print("Please set USE_AI_COMMENTS=true in your .env file")
        return
    
    # Verify provider is OpenRouter
    if os.getenv('AI_PROVIDER', '').lower() != 'openrouter':
        print("❌ AI_PROVIDER is not set to 'openrouter'")
        print("Please set AI_PROVIDER=openrouter in your .env file")
        return
    
    print("🔧 Configuration looks good!")
    print(f"   Provider: {os.getenv('AI_PROVIDER')}")
    print(f"   Model: {os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')}")
    print()
    
    # Initialize components
    image_manager = ImageManager()
    comment_generator = CommentGenerator()
    
    # Get a random image
    image_path = image_manager.get_random_image()
    if not image_path:
        print("❌ No images found in the images directory")
        print("Please add some Lain images to the ./images directory")
        return
    
    print(f"📸 Selected image: {image_path.name}")
    print()
    
    # Generate comment with image analysis
    print("🤖 Generating AI comment based on image content...")
    print("   (This may take a few seconds)")
    print()
    
    try:
        comment = comment_generator.generate_comment(image_path)
        print("✅ Generated comment:")
        print(f"   {comment}")
        print()
        print("🎉 Success! The OpenRouter integration is working correctly.")
        print("   The AI has analyzed the image and generated a contextual comment.")
    except Exception as e:
        print(f"❌ Error generating comment: {e}")
        print("   Check your API key and network connection")

if __name__ == "__main__":
    test_openrouter()

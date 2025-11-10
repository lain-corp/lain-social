# Contributing to Lain Social Bot

Thank you for your interest in contributing to the Lain Social Bot! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Docker version)
- Relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Adding New Social Media Platforms

To add support for a new platform:

1. Create a new file in `social_platforms/` (e.g., `bluesky.py`)
2. Implement a poster class following this template:

```python
"""Platform Name integration."""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PlatformNamePoster:
    """Handler for posting to Platform Name."""

    platform_name = "Platform Name"

    def __init__(self):
        """Initialize API client."""
        # Get credentials from environment
        self.api_key = os.getenv('PLATFORM_API_KEY')
        
        if not self.api_key:
            raise ValueError("Missing Platform credentials")
        
        # Initialize your API client here

    def post(self, image_path: Path, text: str) -> bool:
        """Post image with text.
        
        Args:
            image_path: Path to the image file
            text: Text content for the post
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Implement posting logic here
            logger.info("Successfully posted to Platform Name")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Platform Name: {e}")
            return False
```

3. Add dependencies to `requirements.txt`
4. Update `bot.py` to initialize your poster
5. Update `.env.example` with required environment variables
6. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Add logging for important events

### Testing Your Changes

Before submitting a PR:

1. Test your code locally
2. Verify Docker build works: `docker build -t lain-social-bot:test .`
3. Test with at least one social media platform
4. Check for Python syntax errors: `python -m py_compile *.py`
5. Update documentation as needed

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit with clear messages
5. Push to your fork
6. Create a Pull Request with:
   - Clear description of changes
   - Link to related issues
   - Test results
   - Screenshots if applicable

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/lain-social.git
cd lain-social

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make your changes
# ...

# Test your changes
python bot.py
```

## Code of Conduct

- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards other contributors
- Accept constructive criticism gracefully

## Questions?

Feel free to create an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Let's all love Lain! 💙**

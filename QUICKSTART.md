# Quick Start Guide - Lain Social Bot

This guide will help you get the Lain Social Bot running in under 10 minutes.

## Prerequisites

- Docker installed on your system
- API credentials for at least one social media platform
- At least one Lain Iwakura image

## Step-by-Step Setup

### 1. Clone or Download the Repository

```bash
git clone https://github.com/lain-corp/lain-social.git
cd lain-social
```

### 2. Add Lain Images

Add at least one Lain Iwakura image to the `images/` directory:

```bash
# Example: download a Lain image (make sure you have rights to use it)
# Or copy your own images
cp /path/to/your/lain-image.jpg ./images/
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API credentials for at least one platform:

**Minimum configuration for Twitter:**
```bash
# Basic Settings
RUN_MODE=once  # Use 'once' for testing, 'scheduled' for continuous operation

# Twitter credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Minimum configuration for Mastodon:**
```bash
# Basic Settings
RUN_MODE=once

# Mastodon credentials
MASTODON_ACCESS_TOKEN=your_access_token_here
MASTODON_API_BASE_URL=https://mastodon.social  # or your instance
```

**Minimum configuration for Reddit:**
```bash
# Basic Settings
RUN_MODE=once

# Reddit credentials
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_username_here
REDDIT_PASSWORD=your_password_here
REDDIT_SUBREDDIT=test  # Change to your target subreddit
```

### 4. Run the Bot

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up --build
```

**Option B: Using Docker directly**

```bash
docker build -t lain-social-bot .
docker run --env-file .env -v ./images:/app/images:ro lain-social-bot
```

**Option C: Running locally without Docker**

```bash
pip install -r requirements.txt
python bot.py
```

### 5. Verify the Post

Check your social media platform to see the post!

## Testing with AI Comments (Optional)

To test with AI-generated comments:

1. Get an OpenAI or Anthropic API key
2. Add to your `.env`:

```bash
USE_AI_COMMENTS=true
AI_PROVIDER=openai  # or 'anthropic'
OPENAI_API_KEY=sk-your-key-here
```

3. Run the bot again

## Running Continuously

Once you've tested the bot, switch to scheduled mode:

1. Edit `.env` and change:
```bash
RUN_MODE=scheduled
POST_INTERVAL_HOURS=6  # Post every 6 hours
```

2. Run with Docker Compose:
```bash
docker-compose up -d  # Run in background
```

3. Check logs:
```bash
docker-compose logs -f
```

4. Stop the bot:
```bash
docker-compose down
```

## Troubleshooting

### "No images found"
- Make sure you have image files in the `images/` directory
- Check that files have supported extensions (`.jpg`, `.png`, etc.)

### "No platforms configured"
- Verify you've set API credentials in `.env`
- Check that environment variables are loaded: `docker-compose config`

### API Authentication Errors
- Double-check your API credentials are correct
- Ensure API tokens have necessary permissions
- For Twitter: make sure you have both v1.1 and v2 access

### Docker Build Fails
- Make sure Docker is running
- Check you have internet connectivity for downloading dependencies

## Next Steps

- **Deploy to Akash:** See `README.md` for Akash deployment instructions
- **Add more images:** Keep adding Lain images to the `images/` directory
- **Customize comments:** Edit fallback comments in `ai_comment_generator.py`
- **Add more platforms:** Contributions welcome!

## Getting API Credentials

### Twitter/X
1. Go to https://developer.twitter.com/
2. Create a new app
3. Generate API keys and tokens
4. Enable both v1.1 and v2 API access

### Mastodon
1. Log in to your Mastodon instance
2. Go to Preferences → Development
3. Create a new application
4. Copy the access token

### Reddit
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note the client ID and secret

---

**Present day, present time... 🌐**

Happy posting! Let's all love Lain! 💙

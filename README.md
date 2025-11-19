# Lain Social Bot 🌐

A multi-platform social media bot that automatically posts Lain Iwakura images with AI-generated comments to Twitter/X, Mastodon, and Reddit. Designed to be deployed as a Docker container on Akash Network.

## Features

- **Multi-Platform Support**: Posts simultaneously to Twitter/X, Mastodon, and Reddit
- **AI-Powered Comments**: Optional AI-generated comments using OpenAI or Anthropic
- **Flexible Scheduling**: Run continuously on a schedule or execute once
- **Docker-Ready**: Optimized Docker container for easy deployment
- **Akash Network Compatible**: Deploy on decentralized cloud infrastructure
- **Customizable**: Extensive configuration via environment variables

## Language & Compatibility

This bot is written in **Python 3.11** for maximum compatibility with social media APIs:

- ✅ Twitter/X API (via tweepy)
- ✅ Mastodon API (via Mastodon.py)
- ✅ Reddit API (via praw)
- ✅ OpenAI API (for AI comments)
- ✅ Anthropic API (for AI comments)

Python provides the best ecosystem support for social media integrations with well-maintained, official libraries for all major platforms.

## Quick Start

### Prerequisites

- Docker and Docker Compose (for local testing)
- API credentials for at least one social media platform
- Images of Lain Iwakura in the `images/` directory

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/lain-corp/lain-social.git
   cd lain-social
   ```

2. **Add Lain images**
   ```bash
   # Add your Lain Iwakura images to the images/ directory
   cp /path/to/your/lain-images/* ./images/
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   nano .env
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

### Running Locally Without Docker

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the bot**
   ```bash
   python bot.py
   ```

## Configuration

All configuration is done via environment variables. See `.env.example` for a complete list.

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `RUN_MODE` | `scheduled` | Run mode: `scheduled` for continuous, `once` for single post |
| `POST_INTERVAL_HOURS` | `6` | Hours between posts (scheduled mode only) |
| `SIMULTANEOUS_POST` | `true` | Post to all platforms at once (true) or with delays (false) |
| `IMAGE_DIR` | `./images` | Directory containing Lain images |

### AI Comment Generation (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_AI_COMMENTS` | `false` | Enable AI-generated comments |
| `AI_PROVIDER` | `openai` | AI provider: `openai` or `anthropic` |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model to use |
| `ANTHROPIC_API_KEY` | - | Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-3-haiku-20240307` | Anthropic model to use |

### Social Media Platforms

Configure credentials for the platforms you want to use. The bot will automatically detect and use configured platforms.

#### Twitter/X

Required environment variables:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`

[Get Twitter API credentials](https://developer.twitter.com/)

#### Mastodon

Required environment variables:
- `MASTODON_ACCESS_TOKEN`
- `MASTODON_API_BASE_URL` (default: `https://mastodon.social`)

[Get Mastodon API credentials](https://docs.joinmastodon.org/client/token/)

#### Reddit

Required environment variables:
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USERNAME`
- `REDDIT_PASSWORD`
- `REDDIT_SUBREDDIT` (default: `test`)

[Get Reddit API credentials](https://www.reddit.com/prefs/apps)

### Additional Platforms & Integration Guide

The project includes adapters and placeholders for a broader set of platforms. Below are the environment variables and quick setup notes for each additional platform we support or provide guidance for.

#### LinkedIn

Required environment variables:
- `LINKEDIN_ACCESS_TOKEN` — OAuth2 access token with the `w_member_social` scope (or org-level equivalent)
- `LINKEDIN_OWNER_URN` — Owner URN, e.g. `urn:li:person:xxxxxxxx` or `urn:li:organization:yyyyyyyy`

Notes:
- The bot implements the registerUpload -> binary upload -> `ugcPosts` flow. The access token must be valid and authorized for the owner URN. Organization posting requires admin permissions for that organization.
- See LinkedIn UGC docs: https://learn.microsoft.com/linkedin/marketing/integrations/community-management/shares

#### Facebook (Page photo uploads)

Required environment variables (for Page posting):
- `FB_PAGE_ID` — the numeric Page id
- `FB_PAGE_ACCESS_TOKEN` — Page access token (not just a user token)
- Optional: `FB_GRAPH_VERSION` (default `v17.0`)

Notes:
- The bot uploads local images to the Page via the Graph API `/PAGE_ID/photos` endpoint. You must create a Facebook app and a Page access token with publishing permissions. See: https://developers.facebook.com/docs/pages/publishing/

#### Instagram (Graph API)

Recommended environment variables:
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` — ID of your connected Instagram Business/Creator account
- `FB_PAGE_ACCESS_TOKEN` — the Page access token that has access to the Instagram business account
- `MEDIA_HOSTING_URL` or an S3/Imgur configuration (see Media Hosting below)

Notes:
- Instagram Graph API requires images to be available via a publicly accessible URL (or use the container/publish flow which can accept remote media). The typical flow is:
   1. Upload your local image to a public hosting location (S3/Imgur)
   2. Create an Instagram media container pointing at that URL
   3. Publish the container
- Because the above requires external hosting (or an advanced Graph API flow), the repo includes a placeholder and guidance; we can add an automated hosting helper (S3/Imgur) if you want the bot to post directly from local files.
   See: https://developers.facebook.com/docs/instagram-api/guides/content-publishing

#### TikTok

Integration notes:
- TikTok's Content API requires registering as a developer and creating an app. The API typically needs OAuth authorization and app review for media publishing.
- The repo includes a placeholder module describing the steps; if you want a fully automated flow, provide TikTok app credentials and I can scaffold OAuth and upload code.
   See: https://developers.tiktok.com/

#### Bluesky (AT Protocol)

Integration notes:
- Bluesky uses the AT Protocol (bsky). There are Python/JS clients emerging for interacting with Bluesky. Posting media involves uploading media to Bluesky's blob store then creating a feed post that references the blob.
- The repo includes a placeholder with guidance. If you want a full adapter, I can add an atproto client integration once you provide an app token or credentials.
   See: https://atproto.com/ and https://bsky.app/docs

#### WhatsApp (Cloud API)

Required environment variables:
- `WHATSAPP_PHONE_NUMBER_ID` — the business phone-number-id configured in Meta
- `WHATSAPP_ACCESS_TOKEN` — the WhatsApp Cloud API bearer token
- `WHATSAPP_TO` — destination phone number in international format (e.g. `+15551234567`)

Notes:
- The bot uploads media to `/{phone_number_id}/media` and then sends an image message referencing the returned media id.
- You must set up a WhatsApp Business account on Meta and use the Cloud API. See: https://developers.facebook.com/docs/whatsapp/cloud-api

Alternative (Twilio WhatsApp):
- If you use Twilio's WhatsApp integration, Twilio requires a publicly accessible media URL. Consider using the Media Hosting options below and then using Twilio's REST API with `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and the Twilio WhatsApp sender number (e.g. `whatsapp:+1415xxxxxxx`).

#### Signal

Required environment variables for the current helper:
- `SIGNAL_RECIPIENT` — recipient phone number in international format
- `SIGNAL_CLI_REST_URL` (optional) — URL of a running `signal-cli-rest-api` instance (default `http://localhost:8080`)

Notes:
- Signal has no official central HTTP API. The practical option is to run `signal-cli` (or the `signal-cli-rest-api` wrapper) locally, register a phone number, and expose a REST endpoint the bot can call. The repo includes a helper adapter that attempts common endpoints.
   See: https://github.com/bbernhard/signal-cli-rest-api

#### YouTube

Integration notes:
- YouTube is video-first: posting requires OAuth2 credentials and uploading a video. If you want to create short videos from images (e.g., static image + short audio track), we can add an optional ffmpeg-based video generator and a YouTube uploader that uses OAuth2 refresh tokens.
- Required pieces for a full integration are `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET` and an OAuth flow to obtain `YOUTUBE_REFRESH_TOKEN`.
   See: https://developers.google.com/youtube/v3/guides/uploading_a_video

#### Media Hosting (for platforms that require public URLs)

When a platform requires a public media URL (Instagram, Twilio WhatsApp, some TikTok flows), you can choose one of the following:

- S3 (recommended for production):
   - `AWS_S3_BUCKET`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
   - Upload local images to S3 and use the public URL for API calls.

- Imgur (quick, developer-friendly):
   - `IMGUR_CLIENT_ID` — upload local images to Imgur anonymously and use the returned URL.
   - Note: Imgur has rate limits and terms of service; use appropriately.

We can add a small `media_hosting` helper that uploads files to S3 or Imgur automatically before posting to platforms that require public URLs.

---

If you want, I can implement the media-hosting helper (S3 or Imgur) next and then add a full Instagram and Twilio WhatsApp adapter so the bot can post directly from local images without manual hosting.

## Deployment on Akash Network

### Build and Push Docker Image

1. **Build the Docker image**
   ```bash
   docker build -t yourusername/lain-social-bot:latest .
   ```

2. **Push to Docker Hub**
   ```bash
   docker push yourusername/lain-social-bot:latest
   ```

### Deploy to Akash

1. **Install Akash CLI**
   ```bash
   # Follow instructions at https://docs.akash.network/
   ```

2. **Update deployment configuration**
   ```bash
   # Edit deploy.yaml and update:
   # - Docker image name
   # - Environment variables with your API credentials
   nano deploy.yaml
   ```

3. **Create deployment**
   ```bash
   akash tx deployment create deploy.yaml --from <your-wallet>
   ```

4. **Get deployment details**
   ```bash
   akash query deployment list --owner <your-address>
   ```

5. **Send manifest**
   ```bash
   akash provider send-manifest deploy.yaml --dseq <deployment-sequence>
   ```

For detailed Akash deployment instructions, see the [Akash documentation](https://docs.akash.network/deploy).

## Project Structure

```
lain-social/
├── bot.py                      # Main bot application
├── ai_comment_generator.py     # AI comment generation module
├── image_manager.py            # Image management module
├── social_platforms/           # Social media platform integrations
│   ├── __init__.py
│   ├── twitter.py             # Twitter/X integration
│   ├── mastodon.py            # Mastodon integration
│   └── reddit.py              # Reddit integration
├── images/                     # Directory for Lain images
│   └── README.txt             # Instructions for adding images
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose configuration
├── deploy.yaml                # Akash deployment configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## How It Works

1. **Initialization**: Bot loads configuration and initializes platform clients
2. **Image Selection**: Randomly selects a Lain image from the `images/` directory
3. **Comment Generation**: Generates a comment (AI-powered or from predefined list)
4. **Posting**: Posts to all configured social media platforms
5. **Scheduling**: Waits for the configured interval and repeats (in scheduled mode)

## Adding Images

Place Lain Iwakura images in the `images/` directory. Supported formats:
- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.webp`

**Note**: Ensure you have the right to use and post any images you add. Respect copyright and fair use policies.

## Troubleshooting

### No platforms configured
- Check that you have set API credentials for at least one platform
- Verify environment variables are correctly loaded

### Image not found
- Ensure images are in the `images/` directory
- Check that image files have supported extensions

### API errors
- Verify your API credentials are correct
- Check API rate limits
- Ensure your API tokens have the necessary permissions

### Docker build fails
- Make sure you have Docker installed and running
- Check that all files are present in the directory

## Security Best Practices

- **Never commit API credentials** to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use read-only volume mounts for image directories in production
- Monitor API usage to avoid rate limits and unexpected costs

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Disclaimer

This bot is for educational and personal use. Ensure compliance with:
- Social media platform Terms of Service
- API usage policies
- Copyright laws regarding image posting
- Spam and automation policies

Use responsibly and respect platform guidelines.

## Credits

- Serial Experiments Lain © Yoshitoshi ABe / Pioneer LDC
- Bot created for the Lain community
- Deployed on Akash Network - decentralized cloud infrastructure

---

**Present day, present time... 🌐**

Let's all love Lain! 💙
# Complete Social Media Setup Guide

This guide provides detailed instructions for obtaining API credentials for **all supported social media platforms**.

## Table of Contents

1. [Twitter/X](#twitterx)
2. [Reddit](#reddit)
3. [Discord](#discord)
4. [Telegram](#telegram)
5. [Facebook Page](#facebook-page)
6. [LinkedIn](#linkedin)
7. [WhatsApp Cloud API](#whatsapp-cloud-api)
8. [Signal](#signal)
9. [TikTok](#tiktok-placeholder)
10. [Bluesky](#bluesky-placeholder)

---

## Twitter/X

### Required Credentials
- API Key (Consumer Key)
- API Secret (Consumer Secret)
- Access Token
- Access Token Secret
- Bearer Token

### Setup Steps

1. **Create Twitter Developer Account**
   - Go to https://developer.twitter.com/
   - Sign in with your Twitter account
   - Apply for a developer account (may require approval)

2. **Create a Project and App**
   - Navigate to the Developer Portal
   - Create a new Project
   - Create a new App within the project

3. **Set App Permissions**
   - Go to your App settings
   - Set permissions to "Read and Write"
   - Enable "Request email from users" if needed

4. **Generate Keys and Tokens**
   - Go to "Keys and Tokens" tab
   - Generate API Key and Secret (Consumer Keys)
   - Generate Access Token and Secret
   - Copy the Bearer Token

5. **Add to .env**
   ```bash
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

### Notes
- Free tier has posting limits (check current Twitter API pricing)
- Elevated access may be required for some features

---

## Reddit

### Required Credentials
- Client ID
- Client Secret
- Reddit Username
- Reddit Password
- User Agent (custom name for your bot)
- Subreddit name

### Setup Steps

1. **Create Reddit App**
   - Log in to Reddit
   - Go to https://www.reddit.com/prefs/apps
   - Scroll down and click "Create App" or "Create Another App"

2. **Configure App**
   - Name: "Lain Social Bot"
   - App type: Select "script"
   - Description: "Automated Lain posting bot"
   - About URL: (optional)
   - Redirect URI: http://localhost:8080 (required but not used)
   - Click "Create app"

3. **Get Credentials**
   - Client ID: String under the app name
   - Client Secret: The "secret" field

4. **Add to .env**
   ```bash
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=LainSocialBot/1.0
   REDDIT_SUBREDDIT=test
   ```

### Notes
- Use a test subreddit first (r/test)
- Respect subreddit rules about bot posting
- Some subreddits require moderator approval for bots

---

## Discord

### Required Credentials
- Webhook URL

### Setup Steps

1. **Create Webhook**
   - Open Discord and go to your server
   - Right-click the channel where you want to post
   - Select "Edit Channel"
   - Go to "Integrations" tab
   - Click "Create Webhook" or "View Webhooks"

2. **Configure Webhook**
   - Name: "Lain Bot"
   - Avatar: (optional) Upload a Lain image
   - Channel: Select target channel
   - Click "Copy Webhook URL"

3. **Add to .env**
   ```bash
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/123456789/abcdefghijklmnop
   ```

### Notes
- Simplest integration - no app required
- One webhook per channel
- Can be deleted/regenerated anytime

---

## Telegram

### Required Credentials
- Bot Token
- Chat ID

### Setup Steps

1. **Create Telegram Bot**
   - Open Telegram and search for @BotFather
   - Send `/newbot` command
   - Follow prompts to name your bot
   - Save the Bot Token provided

2. **Get Chat ID**
   
   **Method 1: Using @userinfobot**
   - Search for @userinfobot on Telegram
   - Start a chat and send any message
   - It will reply with your user ID

   **Method 2: Using @getidsbot**
   - Search for @getidsbot on Telegram
   - Start a chat and send any message
   - It will reply with your chat ID

   **Method 3: For Groups/Channels**
   - Add your bot to the group/channel
   - Send a message to the group
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for "chat":{"id": number} in the JSON response
   - Use that number as your Chat ID

3. **Add to .env**
   ```bash
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
   TELEGRAM_CHAT_ID=123456789
   ```

### Notes
- Chat IDs for groups start with a minus sign (e.g., -1001234567890)
- For channels, you need to make the bot an admin
- Private chat IDs are positive numbers

---

## Facebook Page

### Required Credentials
- Page ID
- Page Access Token

### Setup Steps

1. **Create Facebook Developer App**
   - Go to https://developers.facebook.com/
   - Click "My Apps" → "Create App"
   - Choose "Business" or "Consumer" type
   - Fill in app details

2. **Add Facebook Login and Pages API**
   - In app dashboard, add "Facebook Login" product
   - Add "Pages API" or "Instagram Graph API"

3. **Get Page ID**
   - Go to your Facebook Page
   - Click "About"
   - Scroll to find "Page ID" or
   - Check URL: facebook.com/YOUR_PAGE_NAME (then use Graph API Explorer)

4. **Generate Page Access Token**
   - Go to https://developers.facebook.com/tools/explorer/
   - Select your app from dropdown
   - Generate User Access Token with `pages_read_engagement`, `pages_manage_posts`, and `publish_pages` permissions
   - Click "Get Page Access Token" and select your page
   - Copy the Page Access Token

5. **Make Token Long-Lived (Optional)**
   ```bash
   curl -i -X GET "https://graph.facebook.com/v17.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
   ```

6. **Add to .env**
   ```bash
   FB_PAGE_ID=123456789012345
   FB_PAGE_ACCESS_TOKEN=your_page_access_token
   FB_GRAPH_VERSION=v17.0
   ```

### Notes
- Page tokens can be made never-expiring
- Requires app to be in "Live" mode for production
- Test in Development mode first

---

## LinkedIn

### Required Credentials
- Access Token
- Owner URN

### Setup Steps

1. **Create LinkedIn App**
   - Go to https://www.linkedin.com/developers/
   - Click "Create app"
   - Fill in required details
   - Select company page (required)
   - Accept terms and create

2. **Configure App Permissions**
   - In app settings, go to "Auth" tab
   - Request access to `w_member_social` (for personal posts)
   - Or `rw_organization_admin` (for organization posts)
   - Wait for approval if needed

3. **Get OAuth 2.0 Access Token**
   
   **Method 1: Using OAuth 2.0 Flow**
   - Set redirect URI in app settings
   - Build authorization URL:
     ```
     https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=w_member_social
     ```
   - User authorizes and gets code
   - Exchange code for token:
     ```bash
     curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
       -H 'Content-Type: application/x-www-form-urlencoded' \
       -d 'grant_type=authorization_code&code=YOUR_CODE&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&redirect_uri=YOUR_REDIRECT_URI'
     ```

4. **Get Owner URN**
   
   **For Personal Account:**
   ```bash
   curl -X GET https://api.linkedin.com/v2/me \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
   ```
   The response contains your person ID: `urn:li:person:XXXXX`

   **For Organization:**
   ```bash
   curl -X GET https://api.linkedin.com/v2/organizationAcls?q=roleAssignee \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
   ```

5. **Add to .env**
   ```bash
   LINKEDIN_ACCESS_TOKEN=your_access_token
   LINKEDIN_OWNER_URN=urn:li:person:xxxxxxxxxxxxx
   ```

### Notes
- Access tokens expire after 60 days by default
- Refresh tokens can be used for long-lived access
- Organization posting requires admin permissions

---

## WhatsApp Cloud API

### Required Credentials
- Phone Number ID
- Access Token
- Recipient Phone Number

### Setup Steps

1. **Set Up Meta Business Account**
   - Go to https://business.facebook.com/
   - Create a business account if you don't have one

2. **Create WhatsApp App**
   - Go to https://developers.facebook.com/
   - Create a new app → "Business" type
   - Add "WhatsApp" product to your app

3. **Set Up WhatsApp Business Account**
   - Follow the WhatsApp setup flow
   - Verify your business phone number
   - Get your Phone Number ID from the dashboard

4. **Get Access Token**
   - In app dashboard, go to WhatsApp → Getting Started
   - Copy the temporary access token OR
   - Generate a permanent token:
     - Go to Settings → Business Settings → System Users
     - Create a system user
     - Assign WhatsApp permissions
     - Generate token

5. **Add to .env**
   ```bash
   WHATSAPP_PHONE_NUMBER_ID=123456789012345
   WHATSAPP_ACCESS_TOKEN=your_access_token
   WHATSAPP_TO=+15551234567
   ```

### Notes
- Format recipient as international: +[country code][number]
- Free tier includes 1,000 conversations/month
- Requires business verification for production

---

## Signal

### Required Credentials
- Signal CLI REST API URL
- Recipient Phone Number

### Setup Steps

1. **Install signal-cli-rest-api**
   
   **Using Docker (Recommended):**
   ```bash
   docker run -d --name signal-api \
     -p 8080:8080 \
     -v signal-cli-config:/home/.local/share/signal-cli \
     bbernhard/signal-cli-rest-api
   ```

2. **Register Phone Number**
   ```bash
   # Register (you'll receive an SMS)
   curl -X POST http://localhost:8080/v1/register/+15551234567

   # Verify with code from SMS
   curl -X POST http://localhost:8080/v1/register/+15551234567/verify/123456
   ```

3. **Test Connection**
   ```bash
   curl http://localhost:8080/v1/about
   ```

4. **Add to .env**
   ```bash
   SIGNAL_CLI_REST_URL=http://localhost:8080
   SIGNAL_RECIPIENT=+15551234567
   ```

### Notes
- Requires running signal-cli-rest-api service
- Phone number must be registered with Signal
- Recipient must have Signal installed
- See: https://github.com/bbernhard/signal-cli-rest-api

---

## TikTok (Placeholder)

### Status
Currently a placeholder integration. TikTok's Content API requires:

1. **TikTok Developer Account**
   - Apply at https://developers.tiktok.com/
   - Requires business verification

2. **App Registration**
   - Create app in developer portal
   - Request Content Posting API access
   - Wait for approval (can take weeks)

3. **OAuth 2.0 Flow**
   - Implement authorization flow
   - Get user access tokens
   - Use Content Posting API

### Notes
- Complex approval process
- Not suitable for automated bots currently
- Consider using TikTok's scheduling tools instead

---

## Bluesky (Placeholder)

### Status
Currently a placeholder integration. Bluesky uses AT Protocol:

1. **Create Account**
   - Sign up at https://bsky.app/

2. **Get App Password**
   - Go to Settings → App Passwords
   - Create a new app password

3. **Use AT Protocol Client**
   - Install: `pip install atproto`
   - Authenticate with username and app password
   - Post using `app.bsky.feed.post` API

### Implementation Notes
- AT Protocol SDK: https://atproto.com/
- Python client: https://github.com/MarshalX/atproto
- Consider implementing when Bluesky API stabilizes

---

## Quick Reference Table

| Platform | Difficulty | Free Tier | Approval Required | Time to Set Up |
|----------|-----------|-----------|-------------------|----------------|
| Discord | ⭐ Easy | ✅ Yes | ❌ No | 2 minutes |
| Telegram | ⭐ Easy | ✅ Yes | ❌ No | 5 minutes |
| Reddit | ⭐⭐ Medium | ✅ Yes | ❌ No | 5 minutes |
| Twitter/X | ⭐⭐ Medium | ⚠️ Limited | ✅ Sometimes | 15 minutes |
| WhatsApp | ⭐⭐⭐ Hard | ⚠️ Limited | ✅ Yes | 30 minutes |
| Facebook | ⭐⭐⭐ Hard | ✅ Yes | ⚠️ Sometimes | 20 minutes |
| LinkedIn | ⭐⭐⭐ Hard | ✅ Yes | ✅ Sometimes | 30 minutes |
| Signal | ⭐⭐⭐⭐ Advanced | ✅ Yes | ❌ No | 15 minutes + setup |
| TikTok | ⭐⭐⭐⭐⭐ Very Hard | ❌ No | ✅ Yes | Weeks |
| Bluesky | ⭐⭐ Medium | ✅ Yes | ❌ No | 10 minutes |

---

## Recommended Setup Order

### For Beginners
1. Discord (easiest)
2. Telegram
3. Reddit

### For Maximum Reach
1. Twitter/X
2. Discord
3. Telegram
4. Reddit

### For Professional Use
1. LinkedIn
2. Twitter/X
3. Facebook Page

---

## Testing Your Setup

After configuring each platform, test with:

```bash
# Test single post
RUN_MODE=once python bot.py

# Test OpenRouter integration
python test_openrouter.py

# Check for errors
tail -f logs/*.log
```

---

## Troubleshooting

### Common Issues

**"Missing credentials" error**
- Check .env file has all required variables
- Ensure variable names match exactly
- Remove quotes around values

**"Authentication failed"**
- Verify tokens haven't expired
- Check permissions/scopes
- Regenerate tokens if needed

**"Rate limit exceeded"**
- Reduce POST_INTERVAL_HOURS
- Upgrade API tier if available
- Implement exponential backoff

**Posts not appearing**
- Check platform-specific delays
- Verify account isn't shadowbanned
- Review platform posting rules

---

## Security Best Practices

1. **Never commit .env file**
   - Already in .gitignore
   - Use .env.example as template

2. **Rotate tokens regularly**
   - Set reminders for token expiry
   - Use long-lived tokens when available

3. **Use environment-specific configs**
   - Development vs Production .env files
   - Different accounts for testing

4. **Monitor API usage**
   - Track rate limits
   - Set up alerts for errors
   - Review logs regularly

---

## Getting Help

- Check platform documentation links above
- Review bot logs for specific errors
- Open GitHub issue with error details
- Join platform developer communities

---

## Next Steps

After setting up credentials:
1. ✅ Configure OpenRouter for AI comments
2. ✅ Add Lain images to `./images/` directory
3. ✅ Test with `RUN_MODE=once`
4. ✅ Deploy to production
5. ✅ Monitor and optimize

Happy posting! 🌐💙

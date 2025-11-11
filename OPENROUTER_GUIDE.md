# OpenRouter Integration Guide

This guide explains how to use the OpenRouter API integration for multimodal AI-generated comments in the Lain Social Bot.

## What is OpenRouter?

[OpenRouter](https://openrouter.ai/) is a unified API that provides access to multiple AI models from different providers (Anthropic, OpenAI, Google, Meta, etc.) through a single interface. This makes it easy to use vision-capable AI models without managing multiple API keys.

## Why Use OpenRouter?

### Multimodal Capabilities
- **Image Analysis**: The AI can actually "see" your Lain images and generate contextually relevant comments
- **Better Engagement**: Comments are specific to each image rather than generic
- **More Authentic**: The AI understands what's in the picture

### Flexibility
- **Multiple Models**: Switch between different AI models without changing code
- **Cost Optimization**: Choose models based on your budget and quality needs
- **Easy Testing**: Try different models to see which generates the best comments

### Simplified Management
- **One API Key**: Access multiple providers with a single key
- **Unified Pricing**: One bill instead of multiple provider accounts
- **Consistent Interface**: Same API format regardless of underlying model

## Setup Instructions

### 1. Create an OpenRouter Account

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Add credits to your account (pay-as-you-go pricing)

### 2. Get Your API Key

1. Navigate to the [Keys page](https://openrouter.ai/keys)
2. Create a new API key
3. Copy the key (it starts with `sk-or-v1-...`)

### 3. Configure the Bot

Edit your `.env` file and set the following:

```bash
# Enable AI-generated comments
USE_AI_COMMENTS=true

# Use OpenRouter as the provider
AI_PROVIDER=openrouter

# Your OpenRouter API key
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Choose a vision-capable model
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### 4. Test the Integration

Run the test script to verify everything works:

```bash
python test_openrouter.py
```

You should see output like:
```
🔧 Configuration looks good!
   Provider: openrouter
   Model: anthropic/claude-3.5-sonnet

📸 Selected image: lain_01.jpg

🤖 Generating AI comment based on image content...
   (This may take a few seconds)

✅ Generated comment:
   Lain gazes into the digital void, where consciousness becomes code... 🌐💻 #LainIwakura #SerialExperimentsLain

🎉 Success! The OpenRouter integration is working correctly.
   The AI has analyzed the image and generated a contextual comment.
```

## Recommended Models

Here are vision-capable models that work well with the bot:

### Best Quality
- `anthropic/claude-3.5-sonnet` - Best overall, understands anime/visual contexts well
- `anthropic/claude-3-opus` - High quality, more expensive

### Balanced
- `anthropic/claude-3-sonnet` - Good quality, reasonable cost
- `openai/gpt-4-turbo` - GPT-4 with vision capabilities

### Budget-Friendly
- `anthropic/claude-3-haiku` - Fast and cheap, decent quality
- `google/gemini-pro-vision` - Good for high-volume posting

You can see all available models at [OpenRouter Models](https://openrouter.ai/models).

## How It Works

### Without OpenRouter (Text-Only)
```
Random Image → Generic AI Prompt → Generic Comment
"Generate a comment about Lain Iwakura..."
→ "The Wired connects us all... 🌐"
```

### With OpenRouter (Multimodal)
```
Random Image → Image Analysis → Contextual Comment
[Image of Lain at computer] + "Analyze this image..."
→ "Lain merges with the network, her digital self awakening in the glow of screens... 💻✨"
```

## Technical Details

### Image Processing
1. The bot selects a random Lain image
2. The image is encoded to base64
3. The base64 data is sent to OpenRouter with a prompt
4. The vision model analyzes the image
5. A contextual comment is generated and returned

### API Request Format
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze this image and generate a comment..."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
          }
        }
      ]
    }
  ],
  "max_tokens": 150,
  "temperature": 0.9
}
```

## Pricing

OpenRouter uses pay-as-you-go pricing. Costs vary by model:

- **Claude 3.5 Sonnet**: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- **Claude 3 Haiku**: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- **GPT-4 Turbo**: ~$10 per 1M input tokens, ~$30 per 1M output tokens

For social media posts (150 tokens per comment), expect:
- ~$0.0002-0.0005 per comment with Haiku
- ~$0.0005-0.002 per comment with Sonnet
- Posting every 6 hours = ~$0.02-0.30 per month

Check current pricing at [OpenRouter Pricing](https://openrouter.ai/pricing).

## Troubleshooting

### "API key not found" error
- Make sure your `.env` file has `OPENROUTER_API_KEY` set
- Verify the key starts with `sk-or-v1-`
- Check that you've loaded the `.env` file in your deployment

### "Model not found" error
- Verify the model name is correct (check [OpenRouter Models](https://openrouter.ai/models))
- Some models require specific access levels

### "Insufficient credits" error
- Add credits to your OpenRouter account
- Check your balance at [OpenRouter Account](https://openrouter.ai/account)

### Generated comments are too generic
- Try a better model (e.g., Claude 3.5 Sonnet instead of Haiku)
- Adjust the temperature (higher = more creative, lower = more consistent)
- Modify the prompt in `ai_comment_generator.py`

### Rate limiting
- OpenRouter has rate limits per model
- Reduce posting frequency or upgrade your account tier

## Alternative: Fallback to Text-Only

If you want to use OpenRouter but don't need image analysis, you can still use it for text-only generation. Just keep the existing providers (OpenAI/Anthropic) for text-only mode, or modify the code to support text-only OpenRouter requests.

## Support

For issues with:
- **OpenRouter API**: Contact [OpenRouter Support](https://openrouter.ai/support)
- **This Bot**: Open an issue on the GitHub repository
- **Specific Models**: Check the model provider's documentation

## Examples

Here are some real examples of multimodal vs text-only comments:

### Text-Only (Generic)
- "Present day, present time... 🌐 #LainIwakura"
- "No matter where you are, everyone is connected 🔗"

### Multimodal (Image-Aware)
- [Image: Lain at computer] → "Lost in the luminous embrace of the Wired, where reality dissolves into pure information 💻✨ #Lain"
- [Image: Lain with bear costume] → "Even in the analog world, Lain finds comfort in the familiar... before returning to the network 🧸🌐 #SerialExperimentsLain"
- [Image: Close-up of Lain's eyes] → "Through these eyes, she sees both worlds simultaneously—the flesh and the electron 👁️💫 #LainIwakura"

# OpenRouter Quick Start

## 🚀 5-Minute Setup

### 1. Get API Key
```bash
# Visit https://openrouter.ai/
# Sign up → Add credits → Get API key
```

### 2. Configure Bot
```bash
# Edit .env file
USE_AI_COMMENTS=true
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

### 3. Test It
```bash
python test_openrouter.py
```

### 4. Run It
```bash
python bot.py
```

## 📊 Quick Model Comparison

| Model | Quality | Speed | Cost/comment | Best For |
|-------|---------|-------|--------------|----------|
| `anthropic/claude-3.5-sonnet` | ⭐⭐⭐⭐⭐ | Medium | ~$0.001 | **Recommended** - Best quality |
| `anthropic/claude-3-sonnet` | ⭐⭐⭐⭐ | Fast | ~$0.0005 | Balanced performance |
| `anthropic/claude-3-haiku` | ⭐⭐⭐ | Very Fast | ~$0.0002 | High volume posting |
| `openai/gpt-4-turbo` | ⭐⭐⭐⭐ | Slow | ~$0.003 | Alternative to Claude |

## 🎯 What You Get

### Before (Text-Only)
```
"Present day, present time... 🌐 #LainIwakura"
```
*Generic comment, same for every image*

### After (Multimodal)
```
[Image: Lain at computer]
→ "Lost in the digital embrace, where consciousness becomes code 💻✨ #Lain"

[Image: Lain with bear]  
→ "Finding comfort in the analog world before returning to the Wired 🧸🌐 #SerialExperimentsLain"
```
*Contextual comments based on actual image content*

## 💰 Cost Estimate

Posting 4 times per day:
- **Haiku**: $0.02/month
- **Sonnet**: $0.10/month  
- **3.5 Sonnet**: $0.30/month

*Prices approximate, check [openrouter.ai/pricing](https://openrouter.ai/pricing)*

## ⚡ Common Commands

```bash
# Test configuration
python test_openrouter.py

# Run once
RUN_MODE=once python bot.py

# Run scheduled (every 6 hours)
RUN_MODE=scheduled python bot.py

# Check errors
tail -f logs/*.log
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Check `.env` has `OPENROUTER_API_KEY=sk-or-v1-...` |
| "Insufficient credits" | Add credits at [openrouter.ai/account](https://openrouter.ai/account) |
| Generic comments | Change model to Claude 3.5 Sonnet |
| Too expensive | Switch to Haiku or reduce posting frequency |
| No images found | Add images to `./images/` directory |

## 📚 Learn More

- Full guide: `OPENROUTER_GUIDE.md`
- All changes: `CHANGELOG_OPENROUTER.md`
- Main docs: `README.md`
- Get help: GitHub Issues

## 🔑 Required Config

Minimal `.env` for OpenRouter:
```bash
# AI
USE_AI_COMMENTS=true
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-xxxxx
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# At least one platform (example: Discord)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxx

# Images
IMAGE_DIR=./images
```

That's it! You're ready to go. 🎉

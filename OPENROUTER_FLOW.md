# OpenRouter Multimodal Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lain Social Bot                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Bot.py (Main)  │
                    └─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
          ┌──────────────────┐  ┌──────────────────┐
          │ Image Manager    │  │ Comment Generator│
          │ - Select random  │  │ - Choose provider│
          │   Lain image     │  │ - Generate text  │
          └──────────────────┘  └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌─────────────────┐
                    │  generate_post()│
                    └─────────────────┘
                              │
                              ▼
                    Image + Comment created
                              │
                              ▼
                    ┌─────────────────┐
                    │ Post to all     │
                    │ platforms       │
                    └─────────────────┘
```

## Multimodal Comment Generation Flow

```
START: User wants to post
    │
    ▼
┌────────────────────────────┐
│ 1. Select Random Image     │
│    ./images/lain_03.jpg    │
└────────────────────────────┘
    │
    ▼
┌────────────────────────────┐
│ 2. Check AI Provider       │
│    AI_PROVIDER=openrouter? │
└────────────────────────────┘
    │
    ├─── No ──→ Use predefined comments or text-only AI
    │
    ├─── Yes (OpenRouter) ───┐
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 3. Encode Image to Base64  │
    │              │    Read file as binary     │
    │              │    Convert to base64       │
    │              │    Add MIME type prefix    │
    │              └────────────────────────────┘
    │                         │
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 4. Build API Request       │
    │              │  {                         │
    │              │    "model": "claude-3.5",  │
    │              │    "messages": [           │
    │              │      {                     │
    │              │        "content": [        │
    │              │          {"text": "..."},  │
    │              │          {"image": "..."}  │
    │              │        ]                   │
    │              │      }                     │
    │              │    ]                       │
    │              │  }                         │
    │              └────────────────────────────┘
    │                         │
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 5. Send to OpenRouter      │
    │              │  POST /chat/completions    │
    │              │  Authorization: Bearer...  │
    │              └────────────────────────────┘
    │                         │
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 6. AI Analyzes Image       │
    │              │  Vision model processes:   │
    │              │  - Image content           │
    │              │  - Visual elements         │
    │              │  - Context clues           │
    │              │  - Lain characteristics    │
    │              └────────────────────────────┘
    │                         │
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 7. Generate Comment        │
    │              │  Based on what AI "sees"   │
    │              │  + prompt instructions     │
    │              └────────────────────────────┘
    │                         │
    │                         ▼
    │              ┌────────────────────────────┐
    │              │ 8. Return Comment          │
    │              │  "Lain gazes into the      │
    │              │   digital void... 🌐"      │
    │              └────────────────────────────┘
    │                         │
    └─────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ 9. Post Content │
                    │  Image + Comment│
                    │  to all platforms│
                    └─────────────────┘
                              │
                              ▼
                           SUCCESS
```

## Data Flow Detail

### Input: Image File
```
images/lain_wallpaper_01.jpg
├── Size: 156 KB
├── Format: JPEG
├── Dimensions: 1920x1080
└── Content: Lain at computer
```

### Processing: Base64 Encoding
```
Binary Image Data
    ↓
Base64 Encoder
    ↓
"iVBORw0KGgoAAAANSUhEUgAAA..."
    ↓
Data URI Format
    ↓
"data:image/jpeg;base64,iVBORw0KGg..."
```

### API Call: Multimodal Request
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze this image of Lain..."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,..."
          }
        }
      ]
    }
  ],
  "max_tokens": 150,
  "temperature": 0.9
}
```

### Response: AI-Generated Comment
```json
{
  "choices": [
    {
      "message": {
        "content": "Lost in the luminous embrace of the Wired, where reality dissolves into pure information 💻✨ #Lain #SerialExperimentsLain"
      }
    }
  ]
}
```

### Output: Social Media Post
```
┌─────────────────────────────────────┐
│                                     │
│  [Image: lain_wallpaper_01.jpg]     │
│                                     │
│  Lost in the luminous embrace of    │
│  the Wired, where reality dissolves │
│  into pure information 💻✨          │
│  #Lain #SerialExperimentsLain       │
│                                     │
└─────────────────────────────────────┘
```

## Provider Comparison

### Text-Only (OpenAI/Anthropic)
```
Image (unused) ──┐
                 ├──→ Generic Prompt ──→ AI ──→ Generic Comment
Text Prompt ─────┘
```

### Multimodal (OpenRouter)
```
Image ────────┐
              ├──→ Vision Analysis ──→ AI ──→ Contextual Comment
Text Prompt ──┘
```

## Error Handling Flow

```
                API Request
                     │
                     ▼
            ┌────────────────┐
            │ API Call       │
            └────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    Success      Error         Timeout
        │            │            │
        ▼            ▼            ▼
    Return      Log Error    Retry Once
    Comment         │            │
                    ▼            ▼
               Fallback      Success/Fail
               Comments          │
                    │            │
                    └────┬───────┘
                         │
                         ▼
                   Final Comment
```

## Configuration Decision Tree

```
                    START
                      │
                      ▼
            USE_AI_COMMENTS=true?
                      │
            ┌─────────┴─────────┐
            No                 Yes
            │                   │
            ▼                   ▼
    Use Fallback     AI_PROVIDER = ?
    Comments         │
                     ├─── openai ─────→ Text-only GPT
                     │
                     ├─── anthropic ──→ Text-only Claude
                     │
                     └─── openrouter ─→ Multimodal Vision
                                         │
                                         ▼
                                   Image Analysis
                                   Contextual Comments
```

## Cost Flow

```
One Post = One API Call

Cost Components:
├── Input Tokens
│   ├── Text Prompt: ~100 tokens
│   └── Image Data: ~1000 tokens (varies by size)
│       Total Input: ~1100 tokens
│
└── Output Tokens
    └── Generated Comment: ~50 tokens

Total per post:
├── Claude 3.5 Sonnet: ~$0.0015
├── Claude 3 Sonnet: ~$0.0008
└── Claude 3 Haiku: ~$0.0003

Daily (4 posts):
├── Sonnet 3.5: ~$0.006/day = $0.18/month
├── Sonnet 3: ~$0.003/day = $0.09/month
└── Haiku: ~$0.001/day = $0.03/month
```

# JPLensAIContext API

## Objective

An ultra-minimal FastAPI-based AI-powered context analysis service that enhances Japanese text understanding with essential contextual insights. Designed to be used alongside **[JPLENSCONTEXT API](https://github.com/Animenosekai/translate)**

## Features

- **Ultra-minimal responses** - Only essential AI insights
- **Token-efficient** - No wasted AI processing
- **4 key fields only**: natural translation, cultural note, insight, usage example
- **FastAPI REST API** for easy integration
- **Multiple AI providers** (OpenAI GPT and Anthropic Claude)
- **Automatic API documentation** at `/docs`

## Architecture

```
JPLensContext API (OCR + Translation)
        ↓
    JPLensAIContext API (AI Analysis)
        ↓
    Enhanced Understanding with:
    - Natural translations
    - Cultural insights
    - Tone analysis
    - Usage examples
```

## Prerequisites

- Running instance of [JPLensContext API](../JPLensContext)
- OpenAI API key or Claude API key
- Python 3.8+

## Quick Start

### 🚀 **Setup**
```bash
git clone <repository-url>
cd JPLensAIContext
pip install -r requirements.txt
cp .env.example .env
```

### 📋 **Configuration (Required)**
Edit `.env` and set **required fields**:
```bash
AI_PROVIDER=openai  # or "claude"
AI_MODEL=gpt-4      # or "claude-3-sonnet-20240229" for Claude
OPENAI_API_KEY=sk-your-key-here  # or CLAUDE_API_KEY for Claude
```

### 🏃‍♂️ **Run the API**
```bash
python main.py
```

The API will be available at `http://localhost:8001`

### 📖 **API Documentation**
- **Interactive API docs**: http://localhost:8001/docs
- **Alternative docs**: http://localhost:8001/redoc

## API Endpoints

### `POST /analyze`
Main analysis endpoint that accepts structured requests with configuration options.

**Request Body:**
```json
{
  "jplens_data": {
    "ocr": {"text": "ご飯 定食", "confidence": 0.99},
    "translation": {
      "raw_text": "ご飯 定食",
      "literal": "rice set meal"
    }
  },
  "include_cultural_notes": true,
  "include_examples": true
}
```

**Response Body:**
```json
{
  "original_text": "ご飯 定食",
  "basic_translation": {
    "literal": "rice set meal",
    "formality": "unknown"
  },
  "ai_enhanced_analysis": {
    "natural_translation": "Set meal with rice",
    "cultural_note": "In Japanese restaurants, '定食' (teishoku) refers to a set meal, typically including rice, a main dish, miso soup, and side dishes.",
    "insight": "The word 'ご飯' emphasizes that rice is a central component of the meal, reflecting its staple role in Japanese cuisine.",
    "usage_example": {
      "example_japanese": "焼き魚定食",
      "example_english": "Grilled fish set meal"
    }
  },
  "metadata": {
    "analysis_timestamp": "2026-01-08T06:27:16.746154Z",
    "ai_provider": "OpenAI",
    "ai_model_used": "gpt-4.1",
    "cultural_notes_included": true,
    "examples_included": true
  }
}
```

### `POST /analyze/simple`
Simplified endpoint that accepts JPLensContext API response directly.

**Request Body:** (Simplified - only `raw_text` and `literal`)
```json
{
  "ocr": {"text": "ご飯 定食", "confidence": 0.99},
  "translation": {
    "raw_text": "ご飯 定食",
    "literal": "rice set meal"
  }
}
```

**Response:** Same as `/analyze` endpoint above.

### `GET /health`
Health check endpoint.

**Response:**
```json
{"status": "healthy"}
```

### `GET /config`
Get current configuration (safe info only).

**Response:**
```json
{
  "ai_provider": "openai",
  "ai_model": "gpt-4",
  "debug": true,
  "host": "127.0.0.1",
  "port": 8001
}
```

## Integration Example

```python
import requests

# 1. Get data from JPLensContext API
jplens_response = requests.post("http://localhost:8000/translate", ...)

# 2. Send to JPLensAIContext API for enhanced analysis
ai_response = requests.post(
    "http://localhost:8001/analyze/simple",
    json=jplens_response.json()
)

print(ai_response.json())
```

## 🧪 **Testing**
```bash
python demo_ai_analysis.py  # Test the core analysis logic
pytest tests/               # Run unit tests
```

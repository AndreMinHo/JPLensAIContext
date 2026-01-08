# JPLensAIContext

## Objective

A bring-your-own-key AI-powered context analysis service that enhances Japanese text understanding by providing contextual and cultural analysis of Japanese text. Designed to be used with **[JPLENSCONTEXT API](https://github.com/Animenosekai/translate)**

## Features

- Offers a more natural translation of Japanese text
- Provides cultural analysis of the text


## Architecture

```
JPLensContext API (OCR + Translation)
        ↓
    JPLensAIContext API (AI Analysis)
```

## Prerequisites

- Running instance of [JPLensContext API](../JPLensContext)
- OpenAI API key or Claude API key

## Quick Start

### 🚀 **Simple Setup**
```bash
git clone <repository-url>
cd JPLensAIContext
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key and provider choice
```

### 📋 **Configuration (Required)**
Edit `.env` and set **3 things**:
```bash
AI_PROVIDER=openai  # or "claude"
AI_MODEL=gpt-4.1     # specific model (see examples below)
OPENAI_API_KEY=sk-your-key-here  # or CLAUDE_API_KEY for Claude
```


### 🧪 **Test Setup**
```bash
python demo_ai_analysis.py
```

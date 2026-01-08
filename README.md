# JPLensAIContext

## Objective

An AI-powered context analysis service that enhances Japanese text understanding by providing contextual and cultural analysis of Japanese text. Designed to be used with **[JPLENSCONTEXT API](https://github.com/Animenosekai/translate)**

## Features

- Verifies if the literal translation is appropriate for the context
- Provides cultural analysis of Japanese text


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
Edit `.env` and set just **2 things**:
```bash
AI_PROVIDER=openai  # or "claude"
OPENAI_API_KEY=sk-your-key-here  # or CLAUDE_API_KEY for Claude
```

Everything else uses optimized defaults for production use.

### 🧪 **Test Setup**
```bash
python demo_ai_analysis.py
```

## 🔧 **Programmatic Usage**

### **For Other Applications**
```python
from backend.context_analyzer import ContextAnalyzer

# Initialize (reads from .env automatically)
analyzer = ContextAnalyzer()

# Analyze Japanese text with translation data
result = analyzer.analyze_full_context(
    japanese_text="こんにちは、お元気ですか？",
    translation_data={
        "translation": {"literal": "Hello, how are you?"},
        "context": {"formality": "polite"}
    }
)

print(result["ai_enhanced_analysis"]["natural_translation"])
# Output: "Hey there, how are you doing?"
```

### **Environment Variables**
Set these in your deployment environment:
```bash
AI_PROVIDER=openai  # or "claude"
OPENAI_API_KEY=your-key  # or CLAUDE_API_KEY
```

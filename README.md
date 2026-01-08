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
- OpenAI API key (or other LLM provider)

## Quick Start

1. **Clone and setup:**
```bash
git clone <repository-url>
cd JPLensAIContext
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

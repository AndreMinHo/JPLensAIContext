"""AI provider implementations for multiple LLM services"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from unittest.mock import Mock
import openai
import anthropic
from backend.config import settings


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    def analyze_text_context(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str = "unknown"
    ) -> Dict[str, Any]:
        """Analyze Japanese text and provide contextual insights"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model being used"""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider implementation"""

    def __init__(self):
        # Use environment variable approach for better compatibility
        import os
        if not os.environ.get("OPENAI_API_KEY") and settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key

        # Use ai_model if specified, otherwise use provider default
        self.model = settings.ai_model if settings.ai_model and settings.ai_provider == "openai" else settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature

    def get_provider_name(self) -> str:
        return "OpenAI"

    def get_model_name(self) -> str:
        return self.model

    def analyze_text_context(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str = "unknown"
    ) -> Dict[str, Any]:

        prompt = self._build_analysis_prompt(
            japanese_text, literal_translation, formality_level
        )

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in Japanese language and culture. Analyze the given Japanese text and its literal translation to provide deeper contextual understanding, natural translations, and cultural insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response)

        except Exception as e:
            return {
                "error": f"OpenAI analysis failed: {str(e)}",
                "natural_translation": literal_translation,
                "cultural_notes": [],
                "additional_insights": []
            }

    def _build_analysis_prompt(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str
    ) -> str:

        return f"""
Please analyze this Japanese text and provide deeper contextual understanding:

JAPANESE TEXT: "{japanese_text}"
LITERAL TRANSLATION: "{literal_translation}"
DETECTED FORMALITY: {formality_level}

IMPORTANT: Respond ONLY with valid JSON. Do not include any markdown formatting, code blocks, or explanatory text. Just the raw JSON object.

{{
  "natural_translation": "A more natural, contextual English translation",
  "cultural_notes": [
    {{
      "category": "etiquette/social norms/tradition/etc",
      "note": "Detailed explanation of cultural context",
      "relevance": "Why this matters for understanding the text"
    }}
  ],
  "tone_analysis": "Analysis of the emotional tone and speaker intent",
  "usage_examples": [
    {{
      "situation": "Context where similar language would be used",
      "example_japanese": "Example Japanese text",
      "example_english": "English translation",
      "formality_level": "Formality of the example"
    }}
  ],
  "additional_insights": [
    "Any other relevant observations about the text"
  ]
}}

Focus on:
- More natural translations that capture nuance
- Cultural context that might not be obvious
- Social implications and politeness levels
- Common usage patterns and situations
"""

    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse the AI response, handling JSON, markdown, and text formats"""
        import json

        # First try direct JSON parsing
        try:
            result = json.loads(ai_response)
            return result
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code blocks
        if '```json' in ai_response:
            try:
                # Extract content between ```json and the next ```
                start = ai_response.find('```json') + 7
                # Find the next ``` after the start position
                remaining = ai_response[start:]
                end_marker = remaining.find('```')
                if end_marker != -1:
                    json_content = remaining[:end_marker].strip()
                    # Clean up any trailing commas or formatting issues
                    json_content = json_content.rstrip(',')
                    result = json.loads(json_content)
                    return result
            except (json.JSONDecodeError, ValueError) as e:
                # Try alternative extraction if the first method fails
                try:
                    # Look for the JSON object boundaries
                    json_start = ai_response.find('{', ai_response.find('```json'))
                    json_end = ai_response.rfind('}') + 1
                    if json_start != -1 and json_end > json_start:
                        json_content = ai_response[json_start:json_end]
                        result = json.loads(json_content)
                        return result
                except (json.JSONDecodeError, ValueError):
                    pass
                # Debug: print what we tried to parse
                print(f"Debug: Failed to parse JSON from markdown: {e}")
                pass

        # Fallback: extract basic information
        return {
            "natural_translation": ai_response.split('\n')[0] if ai_response else "Analysis failed",
            "cultural_notes": [],
            "tone_analysis": "Unable to parse AI response",
            "usage_examples": [],
            "additional_insights": [ai_response]
        }


class ClaudeProvider(AIProvider):
    """Anthropic Claude provider implementation"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.claude_api_key)
        # Use ai_model if specified, otherwise use provider default
        self.model = settings.ai_model if settings.ai_model and settings.ai_provider == "claude" else settings.claude_model
        self.max_tokens = settings.claude_max_tokens
        self.temperature = settings.claude_temperature

    def get_provider_name(self) -> str:
        return "Claude"

    def get_model_name(self) -> str:
        return self.model

    def analyze_text_context(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str = "unknown"
    ) -> Dict[str, Any]:

        prompt = self._build_analysis_prompt(
            japanese_text, literal_translation, formality_level
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are an expert in Japanese language and culture. Analyze the given Japanese text and its literal translation to provide deeper contextual understanding, natural translations, and cultural insights.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_response = response.content[0].text
            return self._parse_ai_response(ai_response)

        except Exception as e:
            return {
                "error": f"Claude analysis failed: {str(e)}",
                "natural_translation": literal_translation,
                "cultural_notes": [],
                "additional_insights": []
            }

    def _build_analysis_prompt(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str
    ) -> str:

        return f"""
Please analyze this Japanese text and provide deeper contextual understanding:

JAPANESE TEXT: "{japanese_text}"
LITERAL TRANSLATION: "{literal_translation}"
DETECTED FORMALITY: {formality_level}

IMPORTANT: Respond ONLY with valid JSON. Do not include any markdown formatting, code blocks, or explanatory text. Just the raw JSON object.

{{
  "natural_translation": "A more natural, contextual English translation",
  "cultural_notes": [
    {{
      "category": "etiquette/social norms/tradition/etc",
      "note": "Detailed explanation of cultural context",
      "relevance": "Why this matters for understanding the text"
    }}
  ],
  "tone_analysis": "Analysis of the emotional tone and speaker intent",
  "usage_examples": [
    {{
      "situation": "Context where similar language would be used",
      "example_japanese": "Example Japanese text",
      "example_english": "English translation",
      "formality_level": "Formality of the example"
    }}
  ],
  "additional_insights": [
    "Any other relevant observations about the text"
  ]
}}

Focus on:
- More natural translations that capture nuance
- Cultural context that might not be obvious
- Social implications and politeness levels
- Common usage patterns and situations
"""

    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse the AI response, handling JSON, markdown, and text formats"""
        import json

        # First try direct JSON parsing
        try:
            result = json.loads(ai_response)
            return result
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code blocks
        if '```json' in ai_response:
            try:
                # Extract content between ```json and the next ```
                start = ai_response.find('```json') + 7
                # Find the next ``` after the start position
                remaining = ai_response[start:]
                end_marker = remaining.find('```')
                if end_marker != -1:
                    json_content = remaining[:end_marker].strip()
                    result = json.loads(json_content)
                    return result
            except (json.JSONDecodeError, ValueError) as e:
                # Debug: print what we tried to parse
                print(f"Debug: Failed to parse JSON from markdown: {e}")
                pass

        # Fallback: extract basic information
        return {
            "natural_translation": ai_response.split('\n')[0] if ai_response else "Analysis failed",
            "cultural_notes": [],
            "tone_analysis": "Unable to parse AI response",
            "usage_examples": [],
            "additional_insights": [ai_response]
        }


def get_ai_provider() -> AIProvider:
    """Factory function to get the configured AI provider"""
    provider_name = settings.ai_provider.lower()

    # Allow test mode without API keys
    if provider_name == "test":
        return Mock()
    elif provider_name == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY in .env")
        return OpenAIProvider()
    elif provider_name == "claude":
        if not settings.claude_api_key:
            raise ValueError("Claude API key not configured. Set CLAUDE_API_KEY in .env")
        return ClaudeProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {provider_name}. Use 'openai', 'claude', or 'test'")

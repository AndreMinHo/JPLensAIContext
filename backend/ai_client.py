"""OpenAI client for AI-powered text analysis"""

import openai
from typing import Dict, Any, List, Optional
from backend.config import settings


class AIClient:
    """Client for interacting with OpenAI API for text analysis"""

    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature

    def analyze_text_context(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Analyze Japanese text with AI to provide contextual insights.

        Args:
            japanese_text: Original Japanese text
            literal_translation: Direct translation from translation service
            formality_level: Detected formality level (casual, polite, formal)

        Returns:
            Dict containing AI analysis results
        """
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

            # Parse the AI response
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response)

        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "natural_translation": literal_translation,  # Fallback
                "cultural_notes": [],
                "additional_insights": []
            }

    def _build_analysis_prompt(
        self,
        japanese_text: str,
        literal_translation: str,
        formality_level: str
    ) -> str:
        """Build the analysis prompt for the AI"""

        return f"""
Please analyze this Japanese text and provide deeper contextual understanding:

JAPANESE TEXT: "{japanese_text}"
LITERAL TRANSLATION: "{literal_translation}"
DETECTED FORMALITY: {formality_level}

Please provide your analysis in the following JSON format:
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
        """Parse the AI response, handling both JSON and text formats"""
        import json

        try:
            # Try to parse as JSON first
            result = json.loads(ai_response)
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, extract what we can
            return {
                "natural_translation": ai_response.split('\n')[0] if ai_response else "Analysis failed",
                "cultural_notes": [],
                "tone_analysis": "Unable to parse AI response",
                "usage_examples": [],
                "additional_insights": [ai_response]
            }
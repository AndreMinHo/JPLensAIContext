"""Core logic for AI-powered context analysis of Japanese text"""

from typing import Dict, Any, Optional
# Note: AI provider interface is kept for compatibility; actual AI calls are performed via AIClient for easier testing.
from backend.ai_providers import get_ai_provider, AIProvider
from backend.config import settings


class ContextAnalyzer:
    """Analyzes Japanese text context using AI to provide deeper understanding"""

    def __init__(self):
        self.ai_provider: AIProvider = get_ai_provider()
        self.ai_client = None  # Lazy initialization to enable testing via mocks

    def analyze_full_context(
        self,
        japanese_text: str,
        translation_data: Dict[str, Any],
        include_cultural_notes: bool = True,
        include_examples: bool = True
    ) -> Dict[str, Any]:
        """
        Perform complete AI-powered context analysis.

        Args:
            japanese_text: Original Japanese text from OCR
            translation_data: Translation results from JPLensContext API
            include_cultural_notes: Whether to include cultural analysis
            include_examples: Whether to include usage examples

        Returns:
            Complete analysis results
        """
        # Extract key information from translation data
        literal_translation = self._extract_literal_translation(translation_data)
        formality_level = self._extract_formality_level(translation_data)

        # Get AI analysis using the configured provider (OpenAI or Claude)
        ai_analysis = self.ai_provider.analyze_text_context(
            japanese_text=japanese_text,
            literal_translation=literal_translation,
            formality_level=formality_level
        )

        # Structure the complete response
        return {
            "original_text": japanese_text,
            "basic_translation": {
                "literal": literal_translation,
                "formality": formality_level
            },
            "ai_enhanced_analysis": {
                "natural_translation": ai_analysis.get("natural_translation", literal_translation),
                "tone_analysis": ai_analysis.get("tone_analysis", ""),
                "cultural_notes": ai_analysis.get("cultural_notes", []) if include_cultural_notes else [],
                "usage_examples": ai_analysis.get("usage_examples", []) if include_examples else [],
                "additional_insights": ai_analysis.get("additional_insights", [])
            },
            "metadata": {
                "analysis_timestamp": self._get_timestamp(),
                "ai_provider": self.ai_provider.get_provider_name(),
                "ai_model_used": self.ai_provider.get_model_name(),
                "cultural_notes_included": include_cultural_notes,
                "examples_included": include_examples
            }
        }

    def _extract_literal_translation(self, translation_data: Dict[str, Any]) -> str:
        """Extract literal translation from translation data"""
        try:
            translation = translation_data.get("translation", {})
            return translation.get("literal", "Translation not available")
        except (KeyError, TypeError):
            return "Unable to extract translation"

    def _extract_formality_level(self, translation_data: Dict[str, Any]) -> str:
        """Extract formality level from translation data"""
        try:
            context = translation_data.get("context", {})
            return context.get("formality", "unknown")
        except (KeyError, TypeError):
            return "unknown"

    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

    # Sample data methods for testing
    def get_sample_japanese_data(self) -> list[Dict[str, Any]]:
        """Get sample Japanese text data for testing"""
        return [
            {
                "japanese": "こんにちは、お元気ですか？",
                "expected_literal": "Hello, how are you?",
                "expected_formality": "polite",
                "description": "Standard polite greeting"
            },
            {
                "japanese": "ご飯を食べに行きませんか",
                "expected_literal": "Won't you go eat a meal?",
                "expected_formality": "polite",
                "description": "Polite invitation to eat"
            },
            {
                "japanese": "すみません",
                "expected_literal": "Excuse me",
                "expected_formality": "polite",
                "description": "Common polite apology/excuse"
            },
            {
                "japanese": "ありがとうございます",
                "expected_literal": "Thank you",
                "expected_formality": "formal",
                "description": "Formal expression of gratitude"
            }
        ]

    def create_mock_translation_response(
        self,
        japanese_text: str,
        literal_translation: str,
        formality: str = "polite"
    ) -> Dict[str, Any]:
        """Create mock JPLensContext API response for testing"""
        return {
            "raw_text": japanese_text,
            "detected_language": "ja",
            "translation": {
                "literal": literal_translation,
                "natural": literal_translation  # Same for mock
            },
            "context": {
                "usage": "general",
                "formality": formality,
                "cultural_notes": []
            },
            "ambiguity": {
                "is_ambiguous": False,
                "possible_meanings": []
            }
        }

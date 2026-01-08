"""Tests for AI-powered context analysis functionality"""

import pytest
import os
from unittest.mock import Mock, patch
from backend.context_analyzer import ContextAnalyzer

# Set test environment before importing
os.environ['AI_PROVIDER'] = 'test'


class TestContextAnalyzer:
    """Test the core AI context analysis logic"""

    def setup_method(self):
        """Set up test fixtures"""
        # Temporarily set AI provider to "test" mode to avoid API key requirements
        import os
        old_provider = os.environ.get('AI_PROVIDER', 'openai')
        os.environ['AI_PROVIDER'] = 'test'

        try:
            self.analyzer = ContextAnalyzer()
            # Mock the provider methods for testing
            self.analyzer.ai_provider.get_provider_name = Mock(return_value="TestProvider")
            self.analyzer.ai_provider.get_model_name = Mock(return_value="test-model")
            self.analyzer.ai_provider.analyze_text_context = Mock(return_value={
                "natural_translation": "Test translation",
                "cultural_notes": [],
                "tone_analysis": "Test tone",
                "usage_examples": [],
                "additional_insights": []
            })
        finally:
            # Restore original setting
            if 'AI_PROVIDER' in os.environ:
                os.environ['AI_PROVIDER'] = old_provider

    def test_extract_literal_translation(self):
        """Test extraction of literal translation from API response"""
        # Mock JPLensContext API response
        mock_response = {
            "translation": {
                "literal": "Hello, how are you?",
                "natural": "Hey, how's it going?"
            }
        }

        result = self.analyzer._extract_literal_translation(mock_response)
        assert result == "Hello, how are you?"

    def test_extract_formality_level(self):
        """Test extraction of formality level from API response"""
        mock_response = {
            "context": {
                "formality": "polite",
                "usage": "general"
            }
        }

        result = self.analyzer._extract_formality_level(mock_response)
        assert result == "polite"

    def test_create_mock_translation_response(self):
        """Test creation of mock translation response"""
        result = self.analyzer.create_mock_translation_response(
            japanese_text="こんにちは",
            literal_translation="Hello",
            formality="casual"
        )

        assert result["raw_text"] == "こんにちは"
        assert result["detected_language"] == "ja"
        assert result["translation"]["literal"] == "Hello"
        assert result["context"]["formality"] == "casual"

    @patch('backend.ai_client.AIClient.analyze_text_context')
    def test_analyze_full_context_with_mock_ai(self, mock_ai_analyze):
        """Test full context analysis with mocked AI response"""
        # Mock AI response
        mock_ai_analyze.return_value = {
            "natural_translation": "Hey there, how are you doing?",
            "tone_analysis": "Friendly and casual greeting",
            "cultural_notes": [
                {
                    "category": "etiquette",
                    "note": "This is a standard casual greeting",
                    "relevance": "Shows familiarity between speakers"
                }
            ],
            "usage_examples": [
                {
                    "situation": "Greeting a friend",
                    "example_japanese": "こんにちは！",
                    "example_english": "Hello!",
                    "formality_level": "casual"
                }
            ],
            "additional_insights": ["Common in daytime conversations"]
        }

        # Test data
        japanese_text = "こんにちは、お元気ですか？"
        translation_data = self.analyzer.create_mock_translation_response(
            japanese_text=japanese_text,
            literal_translation="Hello, how are you?",
            formality="polite"
        )

        # Run analysis
        result = self.analyzer.analyze_full_context(japanese_text, translation_data)

        # Verify structure
        assert result["original_text"] == japanese_text
        assert result["basic_translation"]["literal"] == "Hello, how are you?"
        assert result["basic_translation"]["formality"] == "polite"

        # Verify AI analysis
        ai_analysis = result["ai_enhanced_analysis"]
        assert ai_analysis["natural_translation"] == "Hey there, how are you doing?"
        assert ai_analysis["tone_analysis"] == "Friendly and casual greeting"
        assert len(ai_analysis["cultural_notes"]) == 1
        assert len(ai_analysis["usage_examples"]) == 1
        assert "Common in daytime conversations" in ai_analysis["additional_insights"]

        # Verify metadata
        assert "analysis_timestamp" in result["metadata"]
        assert result["metadata"]["cultural_notes_included"] is True
        assert result["metadata"]["examples_included"] is True

    def test_analyze_full_context_without_cultural_notes(self):
        """Test analysis with cultural notes disabled"""
        japanese_text = "こんにちは"
        translation_data = self.analyzer.create_mock_translation_response(
            japanese_text=japanese_text,
            literal_translation="Hello",
            formality="casual"
        )

        result = self.analyzer.analyze_full_context(
            japanese_text,
            translation_data,
            include_cultural_notes=False
        )

        assert result["ai_enhanced_analysis"]["cultural_notes"] == []

    def test_analyze_full_context_without_examples(self):
        """Test analysis with usage examples disabled"""
        japanese_text = "こんにちは"
        translation_data = self.analyzer.create_mock_translation_response(
            japanese_text=japanese_text,
            literal_translation="Hello",
            formality="casual"
        )

        result = self.analyzer.analyze_full_context(
            japanese_text,
            translation_data,
            include_examples=False
        )

        assert result["ai_enhanced_analysis"]["usage_examples"] == []

    def test_sample_data_structure(self):
        """Test that sample data has correct structure"""
        samples = self.analyzer.get_sample_japanese_data()

        assert len(samples) > 0

        for sample in samples:
            assert "japanese" in sample
            assert "expected_literal" in sample
            assert "expected_formality" in sample
            assert "description" in sample

            # Test that we can create mock response for each sample
            mock_response = self.analyzer.create_mock_translation_response(
                japanese_text=sample["japanese"],
                literal_translation=sample["expected_literal"],
                formality=sample["expected_formality"]
            )
            assert mock_response["raw_text"] == sample["japanese"]


if __name__ == "__main__":
    pytest.main([__file__])
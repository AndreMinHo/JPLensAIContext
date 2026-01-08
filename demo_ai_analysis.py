#!/usr/bin/env python3
"""
Demo script showing JPLensAIContext analysis with sample data
Run this to see the AI-powered Japanese text analysis in action
"""

import json
from backend.context_analyzer import ContextAnalyzer
from backend.config import settings
from backend.ai_providers import get_ai_provider


def main():
    """Demonstrate AI context analysis with sample Japanese text"""
    print("🤖 JPLensAIContext - AI-Powered Japanese Text Analysis Demo")
    print("=" * 60)

    # Initialize analyzer
    analyzer = ContextAnalyzer()

    # Get sample data
    samples = analyzer.get_sample_japanese_data()

    print(f"📊 Analyzing {len(samples)} sample Japanese texts...")
    print()

    for i, sample in enumerate(samples, 1):
        print(f"🔍 Sample {i}: {sample['description']}")
        print(f"   Japanese: {sample['japanese']}")
        print(f"   Expected: {sample['expected_literal']} ({sample['expected_formality']})")
        print()

        # Create mock translation response (simulating JPLensContext API)
        translation_data = analyzer.create_mock_translation_response(
            japanese_text=sample['japanese'],
            literal_translation=sample['expected_literal'],
            formality=sample['expected_formality']
        )

        # Perform AI analysis
        try:
            result = analyzer.analyze_full_context(
                japanese_text=sample['japanese'],
                translation_data=translation_data
            )

            # Display results
            print("🎯 AI Analysis Results:")
            print(f"   Natural Translation: {result['ai_enhanced_analysis']['natural_translation']}")
            print(f"   Tone: {result['ai_enhanced_analysis']['tone_analysis']}")

            if result['ai_enhanced_analysis']['cultural_notes']:
                print("   🌏 Cultural Notes:")
                for note in result['ai_enhanced_analysis']['cultural_notes'][:2]:  # Show first 2
                    print(f"      • {note['category']}: {note['note']}")

            if result['ai_enhanced_analysis']['usage_examples']:
                print("   💬 Usage Examples:")
                for example in result['ai_enhanced_analysis']['usage_examples'][:1]:  # Show first 1
                    print(f"      • {example['situation']}: '{example['example_japanese']}' → '{example['example_english']}'")

            if result['ai_enhanced_analysis']['additional_insights']:
                print("   💡 Insights:")
                for insight in result['ai_enhanced_analysis']['additional_insights'][:2]:
                    print(f"      • {insight}")

        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")
            print("   💡 Note: Make sure OPENAI_API_KEY is set in .env file")

        print("-" * 60)
        print()

    print("✅ Demo complete!")
    print()
    print("📝 Key Features Demonstrated:")
    print("   • AI-enhanced natural translations")
    print("   • Cultural context analysis")
    print("   • Tone and intent detection")
    print("   • Usage examples and insights")
    print("   • Formality-aware analysis")
    print()
    print("🚀 Ready to integrate into your API!")


if __name__ == "__main__":
    main()
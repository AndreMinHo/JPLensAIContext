#!/usr/bin/env python3
"""
Debug script to test Claude API response directly
"""

from backend.ai_providers import get_ai_provider

def main():
    print("🔍 Debug: Testing Claude AI Response")
    print("=" * 60)
    
    # Get the provider
    provider = get_ai_provider()
    print(f"Provider: {provider.get_provider_name()}")
    print(f"Model: {provider.get_model_name()}")
    print()
    
    # Test with a simple Japanese text
    japanese_text = "こんにちは、お元気ですか？"
    literal_translation = "Hello, how are you?"
    formality_level = "polite"
    
    print(f"Testing with: {japanese_text}")
    print(f"Literal: {literal_translation}")
    print()
    
    try:
        result = provider.analyze_text_context(
            japanese_text=japanese_text,
            literal_translation=literal_translation,
            formality_level=formality_level
        )
        
        print("✅ Analysis Result:")
        print("-" * 60)
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

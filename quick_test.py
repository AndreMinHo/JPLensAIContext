#!/usr/bin/env python3
"""
Quick test with the exact JPLensContext API response format
"""

import requests
import json

# The simplified JPLensContext API response - only raw_text and literal
jplens_response = {
  "ocr": {
    "text": "ご飯 定食",
    "confidence": 0.9919165516812564
  },
  "translation": {
    "raw_text": "ご飯 定食",
    "literal": "rice set meal"
  }
}

def test_with_real_data():
    """Test with the actual JPLensContext response format"""
    print("🧪 Testing with actual JPLensContext API response")
    print("=" * 60)
    print("Input from JPLensContext API:")
    print(json.dumps(jplens_response, indent=2, ensure_ascii=False))
    print("\n" + "=" * 60)

    try:
        response = requests.post(
            "http://localhost:8001/analyze/simple",
            json=jplens_response,
            timeout=30
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n🎯 JPLensAIContext API Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            print("\n📊 Key Results:")
            print(f"   Original Text: {result.get('original_text')}")
            print(f"   Natural Translation: {result.get('ai_enhanced_analysis', {}).get('natural_translation')}")
            print(f"   Cultural Note: {result.get('ai_enhanced_analysis', {}).get('cultural_note')}")
            print(f"   Insight: {result.get('ai_enhanced_analysis', {}).get('insight')}")

            usage_example = result.get('ai_enhanced_analysis', {}).get('usage_example', {})
            if usage_example and usage_example.get('example_japanese'):
                print("   Usage Example:")
                print(f"      Japanese: {usage_example.get('example_japanese')}")
                print(f"      English: {usage_example.get('example_english')}")
            else:
                print("   Usage Example: None")

        else:
            print(f"❌ Error: {response.text}")

    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_with_real_data()

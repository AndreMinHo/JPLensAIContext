#!/usr/bin/env python3
"""
Test script for JPLensAIContext API endpoints
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8001"

def test_root_endpoint():
    """Test the root endpoint"""
    print("🧪 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🧪 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_config_endpoint():
    """Test the config endpoint"""
    print("\n🧪 Testing config endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/config")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_analyze_simple_endpoint():
    """Test the analyze/simple endpoint with sample data"""
    print("\n🧪 Testing analyze/simple endpoint...")

    # Sample JPLensContext API response (simplified - only raw_text and literal)
    sample_data = {
        "ocr": {
            "text": "こんにちは、お元気ですか？",
            "confidence": 0.9919165516812564
        },
        "translation": {
            "raw_text": "こんにちは、お元気ですか？",
            "literal": "Hello, how are you?"
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/analyze/simple",
            json=sample_data,
            timeout=30
        )
        print(f"✅ Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("📄 Analysis Result:")
            print(f"   Original: {result.get('original_text', 'N/A')}")
            print(f"   Natural: {result.get('ai_enhanced_analysis', {}).get('natural_translation', 'N/A')}")
            print(f"   Tone: {result.get('ai_enhanced_analysis', {}).get('tone_analysis', 'N/A')}")
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False

    except Exception as e:
        if isinstance(e, requests.exceptions.Timeout):
            print("❌ Request timed out - AI service may not be configured")
        else:
            print(f"❌ Failed: {e}")
        return False

def test_analyze_with_user_example():
    """Test the analyze/full endpoint with user's provided JPLensContext response example"""
    print("\n🧪 Testing analyze/full with user's JPLensContext response example...")

    # User's provided JPLensContext API response example
    user_example_data = {
        "ocr": {
            "text": "ご飯 定食",
            "confidence": 0.9919165516812564
        },
        "translation": {
            "raw_text": "ご飯 定食",
            "detected_language": "ja",
            "translation": {
                "literal": "rice set meal",
                "natural": "rice set meal"
            },
            "context": {
                "usage": "general",
                "formality": "formal",
                "cultural_notes": []
            },
            "ambiguity": {
                "is_ambiguous": False,
                "possible_meanings": []
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/analyze/full",
            json=user_example_data,
            timeout=30
        )
        print(f"✅ Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("📄 Analysis Result:")
            print(f"   Original: {result.get('original_text', 'N/A')}")
            print(f"   Natural: {result.get('ai_enhanced_analysis', {}).get('natural_translation', 'N/A')}")
            print(f"   Cultural note: {result.get('ai_enhanced_analysis', {}).get('cultural_note', 'N/A')}")
            print(f"   Insight: {result.get('ai_enhanced_analysis', {}).get('insight', 'N/A')}")
            print("\n🔍 Full Response JSON:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False

    except Exception as e:
        if isinstance(e, requests.exceptions.Timeout):
            print("❌ Request timed out - AI service may not be configured")
        else:
            print(f"❌ Failed: {e}")
        return False

def test_analyze_endpoint():
    """Test the main analyze endpoint"""
    print("\n🧪 Testing analyze endpoint...")

    # Sample structured request (simplified)
    sample_request = {
        "jplens_data": {
            "ocr": {
                "text": "ありがとうございます",
                "confidence": 0.95
            },
            "translation": {
                "raw_text": "ありがとうございます",
                "literal": "Thank you"
            }
        },
        "include_cultural_notes": True,
        "include_examples": True
    }

    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=sample_request,
            timeout=30
        )
        print(f"✅ Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("📄 Analysis Result:")
            print(f"   Original: {result.get('original_text', 'N/A')}")
            print(f"   Natural: {result.get('ai_enhanced_analysis', {}).get('natural_translation', 'N/A')}")
            print(f"   Cultural notes: {len(result.get('ai_enhanced_analysis', {}).get('cultural_notes', []))}")
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False

    except Exception as e:
        if isinstance(e, requests.exceptions.Timeout):
            print("❌ Request timed out - AI service may not be configured")
        else:
            print(f"❌ Failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 JPLensAIContext API Test Suite")
    print("=" * 50)

    tests = [
        test_root_endpoint,
        test_health_endpoint,
        test_config_endpoint,
        test_analyze_simple_endpoint,
        test_analyze_with_user_example,
        test_analyze_endpoint
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check API configuration.")

    print("\n💡 Note: AI analysis tests may fail if API keys are not configured")
    print("   Check your .env file for OPENAI_API_KEY or CLAUDE_API_KEY")


if __name__ == "__main__":
    main()

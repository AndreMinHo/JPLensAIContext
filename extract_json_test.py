#!/usr/bin/env python3
"""
Test JSON extraction from Claude response
"""

# Sample Claude response from debug
sample_response = '''```json
{
  "natural_translation": "Hi there" or "Hello" (depending on context and relationship)",
  "cultural_notes": [
    {
      "category": "etiquette/social norms",
      "note": "こんにちは is the standard daytime greeting in Japanese, literally meaning 'this is the afternoon' (今日 konnichi = this day/afternoon, は = topic marker). It evolved from a more formal acknowledgment of time of day into a universal greeting.",
      "relevance": "Understanding the etymology reveals how Japanese greetings are rooted in temporal awareness and seasonal consciousness, reflecting the culture's attention to context and timing."
    }
  ],
  "tone_analysis": "The tone is friendly, neutral, and appropriately respectful",
  "usage_examples": [
    {
      "situation": "Meeting a colleague at the office",
      "example_japanese": "こんにちは",
      "example_english": "Hello",
      "formality_level": "polite"
    }
  ],
  "additional_insights": [
    "This is a common greeting"
  ]
}
```'''

print('Testing JSON extraction from Claude response...')
print('=' * 50)

# Method 1: Current parsing logic
if '```json' in sample_response:
    try:
        start = sample_response.find('```json') + 7
        remaining = sample_response[start:]
        end_marker = remaining.find('```')
        if end_marker != -1:
            json_content = remaining[:end_marker].strip()
            print('Extracted JSON content:')
            print(json_content[:200] + '...')
            print()

            import json
            result = json.loads(json_content)
            print('✅ Successfully parsed JSON!')
            print(f'Natural translation: {result["natural_translation"]}')
            print(f'Cultural notes: {len(result["cultural_notes"])}')

    except Exception as e:
        print(f'❌ Failed: {e}')

# Method 2: Alternative extraction
try:
    json_start = sample_response.find('{', sample_response.find('```json'))
    json_end = sample_response.rfind('}') + 1
    if json_start != -1 and json_end > json_start:
        json_content = sample_response[json_start:json_end]
        print('\\nAlternative extraction:')
        print(json_content[:200] + '...')

        import json
        result = json.loads(json_content)
        print('✅ Alternative method worked!')
        print(f'Natural translation: {result["natural_translation"]}')

except Exception as e:
    print(f'❌ Alternative failed: {e}')
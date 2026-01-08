#!/usr/bin/env python3
"""
Test Claude with fixed JSON parsing
"""

from backend.context_analyzer import ContextAnalyzer

print('🤖 Testing Claude with Fixed JSON Parsing')
print('=' * 50)

try:
    analyzer = ContextAnalyzer()
    print('✅ Claude provider initialized')
    print(f'   Provider: {analyzer.ai_provider.get_provider_name()}')
    print(f'   Model: {analyzer.ai_provider.get_model_name()}')

    test_data = analyzer.create_mock_translation_response('こんにちは', 'Hello', 'polite')

    print()
    print('🚀 Making API call to Claude with fixed parsing...')
    result = analyzer.analyze_full_context('こんにちは', test_data)

    print('✅ Claude API call successful!')
    analysis = result['ai_enhanced_analysis']
    print(f'   Natural translation: "{analysis["natural_translation"]}"')
    print(f'   Cultural notes: {len(analysis["cultural_notes"])} items')
    print(f'   Usage examples: {len(analysis["usage_examples"])} items')

    if analysis['cultural_notes']:
        print('   📚 Rich cultural analysis detected!')
        for i, note in enumerate(analysis['cultural_notes'][:2]):
            category = note.get('category', 'Unknown')
            note_text = note.get('note', '')[:80]
            print(f'      {i+1}. {category}: {note_text}...')

    if analysis['tone_analysis']:
        tone = analysis['tone_analysis'][:100]
        print(f'   🎭 Tone: {tone}...')

except Exception as e:
    print(f'❌ Error: {str(e)}')
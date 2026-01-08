"""Pydantic schemas for JPLensAIContext API"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class JPLensTranslation(BaseModel):
    """Translation data from JPLensContext API"""
    literal: str = Field(..., description="Literal/direct translation")
    natural: Optional[str] = Field(None, description="Natural translation if available")


class JPLensContext(BaseModel):
    """Context information from JPLensContext API"""
    usage: str = Field(..., description="Usage context (general, formal, etc.)")
    formality: str = Field(..., description="Formality level (formal, polite, casual)")
    cultural_notes: List[str] = Field(default_factory=list, description="Cultural notes")


class JPLensAmbiguity(BaseModel):
    """Ambiguity information from JPLensContext API"""
    is_ambiguous: bool = Field(..., description="Whether the text has multiple meanings")
    possible_meanings: List[str] = Field(default_factory=list, description="Possible alternative meanings")


class JPLensSimpleTranslation(BaseModel):
    """Simplified translation section from JPLensContext API - only raw_text and literal"""
    raw_text: str = Field(..., description="Raw Japanese text")
    literal: str = Field(..., description="Literal/direct translation")

class JPLensSimpleResponse(BaseModel):
    """Simplified response from JPLensContext API - only OCR text and basic translation"""
    ocr: Dict[str, Any] = Field(..., description="OCR results")
    translation: JPLensSimpleTranslation = Field(..., description="Simplified translation section")


class UsageExample(BaseModel):
    """Single usage example with Japanese and English"""
    example_japanese: str = Field(..., description="Example Japanese text")
    example_english: str = Field(..., description="English translation of the example")


class AIAnalysisResponse(BaseModel):
    """Minimal AI-enhanced analysis response with only essential fields"""
    natural_translation: str = Field(..., description="More natural, contextual English translation")
    cultural_note: str = Field(..., description="Single cultural context note")
    insight: str = Field(..., description="Single additional insight")
    usage_example: UsageExample = Field(..., description="Single usage example")


class BasicTranslation(BaseModel):
    """Basic translation information"""
    literal: str = Field(..., description="Literal translation")
    formality: str = Field(..., description="Formality level")


class Metadata(BaseModel):
    """Analysis metadata"""
    analysis_timestamp: str = Field(..., description="When the analysis was performed")
    ai_provider: str = Field(..., description="AI provider used (OpenAI, Claude)")
    ai_model_used: str = Field(..., description="Specific AI model used")
    cultural_notes_included: bool = Field(..., description="Whether cultural notes were included")
    examples_included: bool = Field(..., description="Whether usage examples were included")


class AnalysisRequest(BaseModel):
    """Request to analyze Japanese text context"""
    jplens_data: JPLensSimpleResponse = Field(..., description="Data from JPLensContext API")
    include_cultural_notes: bool = Field(True, description="Whether to include cultural analysis")
    include_examples: bool = Field(True, description="Whether to include usage examples")


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    original_text: str = Field(..., description="Original Japanese text")
    basic_translation: BasicTranslation = Field(..., description="Basic translation information")
    ai_enhanced_analysis: AIAnalysisResponse = Field(..., description="AI-enhanced analysis")
    metadata: Metadata = Field(..., description="Analysis metadata")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z", description="Error timestamp")

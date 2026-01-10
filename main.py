"""FastAPI application for JPLensAIContext - AI-powered Japanese text analysis"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any

from backend.context_analyzer import ContextAnalyzer
from backend.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    ErrorResponse,
    JPLensSimpleResponse,
    JPLensFullResponse
)
from backend.config import settings


# Initialize FastAPI app
app = FastAPI(
    title="JPLensAIContext API",
    description="AI-powered context analysis service for Japanese text understanding",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get context analyzer
def get_context_analyzer() -> ContextAnalyzer:
    """Dependency injection for ContextAnalyzer"""
    return ContextAnalyzer()


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {
        "name": "JPLensAIContext API",
        "description": "AI-powered Japanese text context analysis",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_context(
    request: AnalysisRequest,
    analyzer: ContextAnalyzer = Depends(get_context_analyzer)
) -> AnalysisResponse:
    """
    Analyze Japanese text context using AI enhancement.

    This endpoint takes simplified data from JPLensContext API (only raw_text and literal)
    and provides AI-powered analysis with cultural insights.
    """
    try:
        # Extract Japanese text from OCR data
        japanese_text = request.jplens_data.ocr.get("text", "")
        if not japanese_text:
            raise HTTPException(
                status_code=400,
                detail="No Japanese text found in OCR data"
            )

        # Create simplified translation data structure with only raw_text and literal
        translation_data = {
            "translation": {
                "literal": request.jplens_data.translation.literal,
                "natural": request.jplens_data.translation.literal  # Use literal as fallback
            },
            "context": {
                "usage": "general",
                "formality": "unknown",  # Default since we don't have this info
                "cultural_notes": []
            },
            "ambiguity": {
                "is_ambiguous": False,
                "possible_meanings": []
            }
        }

        # Perform analysis
        result = analyzer.analyze_full_context(
            japanese_text=japanese_text,
            translation_data=translation_data,
            include_cultural_notes=request.include_cultural_notes,
            include_examples=request.include_examples
        )

        # Convert result to Pydantic model
        return AnalysisResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/analyze/simple")
async def analyze_simple(
    jplens_data: JPLensSimpleResponse,
    analyzer: ContextAnalyzer = Depends(get_context_analyzer)
) -> Dict[str, Any]:
    """
    Simple analysis endpoint that accepts JPLensContext response directly.

    This endpoint only uses raw_text and literal translation from JPLensContext API.
    """
    try:
        # Extract Japanese text from OCR data
        japanese_text = jplens_data.ocr.get("text", "")
        if not japanese_text:
            raise HTTPException(
                status_code=400,
                detail="No Japanese text found in OCR data"
            )

        # Create simplified translation data structure with only raw_text and literal
        translation_data = {
            "translation": {
                "literal": jplens_data.translation.literal,
                "natural": jplens_data.translation.literal  # Use literal as fallback
            },
            "context": {
                "usage": "general",
                "formality": "unknown",  # Default since we don't have this info
                "cultural_notes": []
            },
            "ambiguity": {
                "is_ambiguous": False,
                "possible_meanings": []
            }
        }

        # Perform analysis with defaults
        result = analyzer.analyze_full_context(
            japanese_text=japanese_text,
            translation_data=translation_data,
            include_cultural_notes=True,
            include_examples=True
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/analyze/full")
async def analyze_full(
    jplens_data: JPLensFullResponse,
    analyzer: ContextAnalyzer = Depends(get_context_analyzer)
) -> Dict[str, Any]:
    """
    Full analysis endpoint that accepts complete JPLensContext response.

    This endpoint uses all available data from JPLensContext API including context and ambiguity info.
    """
    try:
        # Extract Japanese text from OCR data
        japanese_text = jplens_data.ocr.get("text", "")
        if not japanese_text:
            raise HTTPException(
                status_code=400,
                detail="No Japanese text found in OCR data"
            )

        # Use the full translation data structure from the API response
        translation_data = {
            "translation": {
                "literal": jplens_data.translation.translation.literal,
                "natural": jplens_data.translation.translation.natural or jplens_data.translation.translation.literal
            },
            "context": {
                "usage": jplens_data.translation.context.usage,
                "formality": jplens_data.translation.context.formality,
                "cultural_notes": jplens_data.translation.context.cultural_notes
            },
            "ambiguity": {
                "is_ambiguous": jplens_data.translation.ambiguity.is_ambiguous,
                "possible_meanings": jplens_data.translation.ambiguity.possible_meanings
            }
        }

        # Perform analysis with defaults
        result = analyzer.analyze_full_context(
            japanese_text=japanese_text,
            translation_data=translation_data,
            include_cultural_notes=True,
            include_examples=True
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get current configuration (safe info only)"""
    return {
        "ai_provider": settings.ai_provider,
        "ai_model": settings.ai_model,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port
    }


if __name__ == "__main__":
    # Use 0.0.0.0 for production/Railway deployment
    host = "0.0.0.0" if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PORT") else settings.host
    uvicorn.run(
        "main:app",
        host=host,
        port=settings.port,
        reload=settings.debug
    )

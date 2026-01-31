"""
AI-Powered Scam Detection API
FastAPI backend for analyzing audio call transcripts and detecting scam patterns
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="AI Scam Detection API",
    description="Analyzes call data to detect potential scam patterns",
    version="1.0.0"
)

# ============================================================================
# PYDANTIC MODELS FOR REQUEST AND RESPONSE VALIDATION
# ============================================================================

class CallAnalysisRequest(BaseModel):
    """
    Request model for call analysis endpoint.
    Validates input data and ensures all scores are within valid range (0-100).
    """
    transcript: str = Field(..., description="The text transcript of the call")
    keyword_score: float = Field(..., ge=0, le=100, description="Keyword detection score (0-100)")
    ml_probability: float = Field(..., ge=0, le=100, description="ML scam probability score (0-100)")
    voice_stress_score: float = Field(..., ge=0, le=100, description="Voice stress analysis score (0-100)")
    
    @validator('transcript')
    def transcript_not_empty(cls, v):
        """Ensure transcript is not empty"""
        if not v or not v.strip():
            raise ValueError('Transcript cannot be empty')
        return v


class CallAnalysisResponse(BaseModel):
    """
    Response model for call analysis endpoint.
    Returns comprehensive analysis results including risk score and alert.
    """
    final_risk_score: float = Field(..., description="Calculated final risk score (0-100)")
    risk_label: str = Field(..., description="Risk category: Safe, Suspicious, or Scam")
    transcript: str = Field(..., description="Original call transcript")
    detected_keywords_score: float = Field(..., description="Keyword detection score")
    ml_scam_probability: float = Field(..., description="ML-based scam probability")
    voice_stress_score: float = Field(..., description="Voice stress analysis score")
    voice_alert_message: str = Field(..., description="Alert message for the user")


# ============================================================================
# RISK SCORING LOGIC
# ============================================================================

def calculate_risk_score(keyword_score: float, ml_probability: float, voice_stress_score: float) -> float:
    """
    Calculate the final risk score using weighted formula.
    
    Formula: FinalRiskScore = (Keyword Score × 0.4) + (ML Probability × 0.5) + (Voice Stress × 0.1)
    
    Args:
        keyword_score: Keyword detection score (0-100)
        ml_probability: ML scam probability (0-100)
        voice_stress_score: Voice stress score (0-100)
    
    Returns:
        Final risk score (0-100)
    """
    final_score = (
        (keyword_score * 0.4) +
        (ml_probability * 0.5) +
        (voice_stress_score * 0.1)
    )
    
    # Ensure the score stays within 0-100 range
    return round(min(max(final_score, 0), 100), 2)


def determine_risk_label(risk_score: float) -> str:
    """
    Determine risk category based on the final risk score.
    
    Risk Levels:
    - 0-30: Safe
    - 31-70: Suspicious
    - 71-100: Scam
    
    Args:
        risk_score: The calculated final risk score
    
    Returns:
        Risk label string
    """
    if risk_score <= 30:
        return "Safe"
    elif risk_score <= 70:
        return "Suspicious"
    else:
        return "Scam"


def generate_voice_alert(risk_label: str) -> str:
    """
    Generate appropriate voice alert message based on risk label.
    
    Args:
        risk_label: The determined risk category (Safe, Suspicious, or Scam)
    
    Returns:
        Voice alert message string
    """
    alert_messages = {
        "Safe": "This call appears safe.",
        "Suspicious": "Warning. This call shows suspicious scam patterns.",
        "Scam": "Danger! This call is highly likely to be a scam."
    }
    
    return alert_messages.get(risk_label, "Unable to determine risk level.")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/analyze-call", response_model=CallAnalysisResponse)
async def analyze_call(request: CallAnalysisRequest):
    """
    Analyze a call transcript and associated metrics to detect scam patterns.
    
    This endpoint processes the input data through multiple analysis stages:
    1. Validates input data using Pydantic models
    2. Calculates weighted risk score using the formula
    3. Determines risk category (Safe, Suspicious, Scam)
    4. Generates appropriate voice alert message
    5. Returns comprehensive analysis results
    
    Args:
        request: CallAnalysisRequest containing transcript and analysis scores
    
    Returns:
        CallAnalysisResponse with complete analysis results
    
    Raises:
        HTTPException: If there's an error during processing
    """
    try:
        # Step 1: Calculate the final risk score using weighted formula
        final_risk_score = calculate_risk_score(
            keyword_score=request.keyword_score,
            ml_probability=request.ml_probability,
            voice_stress_score=request.voice_stress_score
        )
        
        # Step 2: Determine the risk label based on the calculated score
        risk_label = determine_risk_label(final_risk_score)
        
        # Step 3: Generate voice alert message based on risk level
        voice_alert_message = generate_voice_alert(risk_label)
        
        # Step 4: Prepare and return the response
        response = CallAnalysisResponse(
            final_risk_score=final_risk_score,
            risk_label=risk_label,
            transcript=request.transcript,
            detected_keywords_score=request.keyword_score,
            ml_scam_probability=request.ml_probability,
            voice_stress_score=request.voice_stress_score,
            voice_alert_message=voice_alert_message
        )
        
        return response
        
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing call analysis: {str(e)}"
        )


@app.get("/")
async def root():
    """
    Root endpoint to verify API is running.
    
    Returns:
        Welcome message with API information
    """
    return {
        "message": "AI Scam Detection API is running",
        "version": "1.0.0",
        "endpoints": {
            "analyze_call": "/analyze-call (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        Health status of the API
    """
    return {"status": "healthy"}


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run the application using uvicorn
    # Command: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

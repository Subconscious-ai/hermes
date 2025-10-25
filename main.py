import json
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Hermes Campaign Generator API",
    description="AI co-pilot for marketers that transforms email campaign creation from guesswork into a science",
    version="1.0.0"
)

# Enable CORS for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class CampaignRequest(BaseModel):
    product_description: str
    target_audience_urls: List[str]
    messaging_angles: Optional[List[str]] = []

class EmailContent(BaseModel):
    email_number: int
    subject: str
    preview_text: str
    body: str
    cta: str

class CampaignResponse(BaseModel):
    id: str
    created_at: str
    product_description: str
    target_audience_urls: List[str]
    winning_insight_summary: str
    full_subconscious_results: dict
    final_llm_prompt: str
    generated_campaign: List[EmailContent]

# Routes
@app.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Hermes Campaign Generator",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/generate-campaign-mock", response_model=CampaignResponse)
def generate_campaign_mock(request: CampaignRequest):
    """
    Mock endpoint that returns hardcoded perfect data.
    This enables parallel frontend development while the real backend is being built.
    """
    try:
        # Load mock response
        with open("mock_response.json", "r", encoding="utf-8") as f:
            mock_data = json.load(f)
        
        # Override with user's actual input for realism
        mock_data["product_description"] = request.product_description
        mock_data["target_audience_urls"] = request.target_audience_urls
        mock_data["created_at"] = datetime.utcnow().isoformat() + "Z"
        
        return mock_data
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Mock response file not found. Please ensure mock_response.json exists."
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid JSON in mock response file."
        )

@app.post("/generate-campaign", response_model=CampaignResponse)
def generate_campaign(request: CampaignRequest):
    """
    Real endpoint for campaign generation.
    This will be implemented in Phase 2 with Subconscious API, OpenAI, and Supabase integration.
    """
    raise HTTPException(
        status_code=501,
        detail="Real implementation coming in Phase 2. Please use /generate-campaign-mock for now."
    )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

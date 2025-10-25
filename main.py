import json
import os
import time
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import our custom modules
from mock_subconscious import generate_mock_subconscious_response
from reasoning_layer import summarize_results, build_openai_prompt, extract_emails_from_openai_response
from openai_client import OpenAIClient
from supabase_client import save_complete_campaign

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Hermes Campaign Generator API",
    description="AI co-pilot for marketers that transforms email campaign creation from guesswork into a science",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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
def root():
    """Serve the frontend"""
    return FileResponse("static/index.html")

@app.get("/health")
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
async def generate_campaign(request: CampaignRequest):
    """
    Real endpoint for campaign generation with full workflow:
    1. Call Subconscious API (or mock) to get behavioral insights
    2. Extract winning insights and build OpenAI prompt
    3. Call OpenAI GPT-4 to generate email campaign
    4. Save complete workflow to Supabase
    5. Return generated campaign
    """
    start_time = time.time()
    
    try:
        # === STEP 1: Get behavioral insights from Subconscious ===
        # For now, we use mock data. When you get API access, replace this with:
        # subconscious_response = call_real_subconscious_api(...)
        
        subconscious_response = generate_mock_subconscious_response(
            product_description=request.product_description,
            target_audience_urls=request.target_audience_urls,
            messaging_angles=request.messaging_angles if request.messaging_angles else None
        )
        
        # === STEP 2: Extract insights and build OpenAI prompt ===
        summary = summarize_results(subconscious_response)
        
        openai_prompt = build_openai_prompt(
            product_description=request.product_description,
            summary=summary,
            num_emails=3
        )
        
        # === STEP 3: Call OpenAI to generate campaign ===
        openai_client = OpenAIClient()
        openai_result = openai_client.generate_campaign(
            prompt=openai_prompt,
            temperature=0.7,
            max_tokens=3000
        )
        
        # Parse emails from OpenAI response
        emails, campaign_strategy = extract_emails_from_openai_response(
            openai_result["content"]
        )
        
        # === STEP 4: Save to Supabase ===
        # Only save if Supabase credentials are configured
        campaign_record = None
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
            try:
                campaign_record = save_complete_campaign(
                    product_description=request.product_description,
                    target_audience_urls=request.target_audience_urls,
                    subconscious_data=subconscious_response,
                    openai_prompt=openai_prompt,
                    openai_response=openai_result["content"],
                    openai_tokens=openai_result["tokens_used"],
                    openai_cost=openai_result["cost_usd"],
                    emails=emails,
                    campaign_strategy=campaign_strategy,
                    duration_seconds=time.time() - start_time
                )
            except Exception as db_error:
                # Log error but don't fail the request
                print(f"Warning: Failed to save to Supabase: {db_error}")
        
        # === STEP 5: Format and return response ===
        # Convert emails to response format
        formatted_emails = [
            EmailContent(
                email_number=email["email_number"],
                subject=email["subject_line"],
                preview_text=email["subject_line"],  # Use subject as preview
                body=email["email_body"],
                cta=email["cta_text"]
            )
            for email in emails
        ]
        
        # Build response
        response = CampaignResponse(
            id=campaign_record["id"] if campaign_record else subconscious_response["experiment_id"],
            created_at=datetime.utcnow().isoformat() + "Z",
            product_description=request.product_description,
            target_audience_urls=request.target_audience_urls,
            winning_insight_summary=summary["winning_insight"],
            full_subconscious_results=subconscious_response,
            final_llm_prompt=openai_prompt,
            generated_campaign=formatted_emails
        )
        
        return response
        
    except ValueError as e:
        # Missing API keys or configuration issues
        raise HTTPException(
            status_code=400,
            detail=f"Configuration error: {str(e)}. Please check your .env file."
        )
    
    except RuntimeError as e:
        # API call failures
        raise HTTPException(
            status_code=502,
            detail=f"External API error: {str(e)}"
        )
    
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

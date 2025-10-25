"""
Supabase Integration Module

Handles all database operations for the Hermes campaign generator.
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class SupabaseClient:
    """Wrapper for Supabase database operations."""
    
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize Supabase client.
        
        Args:
            url: Supabase project URL (defaults to SUPABASE_URL env var)
            key: Supabase API key (defaults to SUPABASE_KEY env var)
        """
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError(
                "Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY "
                "environment variables or pass as parameters."
            )
        
        self.client: Client = create_client(self.url, self.key)
    
    
    def create_campaign(
        self,
        product_description: str,
        target_audience_urls: List[str]
    ) -> Dict[str, Any]:
        """
        Create a new campaign record with 'pending' status.
        
        Args:
            product_description: Product/service description
            target_audience_urls: LinkedIn profile URLs
            
        Returns:
            Created campaign record
        """
        try:
            campaign_data = {
                "product_description": product_description,
                "target_audience_urls": target_audience_urls,
                "status": "pending",
                "generated_campaign": []  # Initialize with empty array
            }
            
            response = self.client.table("campaigns").insert(campaign_data).execute()
            
            if not response.data:
                raise RuntimeError("Failed to create campaign record")
            
            return response.data[0]
            
        except Exception as e:
            raise RuntimeError(f"Database error creating campaign: {str(e)}")
    
    
    def update_campaign_status(
        self,
        campaign_id: int,
        status: str,
        error_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update campaign status.
        
        Args:
            campaign_id: Campaign ID
            status: New status (pending, processing, completed, failed)
            error_message: Optional error message if status is 'failed'
            
        Returns:
            Updated campaign record
        """
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            if error_message:
                update_data["error_message"] = error_message
            
            response = self.client.table("campaigns").update(update_data).eq("id", campaign_id).execute()
            
            if not response.data:
                raise RuntimeError(f"Campaign {campaign_id} not found")
            
            return response.data[0]
            
        except Exception as e:
            raise RuntimeError(f"Database error updating campaign status: {str(e)}")
    
    
    def save_subconscious_results(
        self,
        campaign_id: int,
        experiment_id: str,
        request_payload: Dict[str, Any],
        response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save Subconscious API request and response.
        
        Args:
            campaign_id: Campaign ID
            experiment_id: Subconscious experiment ID
            request_payload: Request sent to Subconscious
            response_data: Response from Subconscious
            
        Returns:
            Updated campaign record
        """
        try:
            # Extract mindset segments for easy querying
            mindset_segments = response_data.get("mindset_segments", [])
            
            update_data = {
                "status": "processing",
                "subconscious_experiment_id": experiment_id,
                "subconscious_request": request_payload,
                "subconscious_response": response_data,
                "mindset_segments": mindset_segments,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table("campaigns").update(update_data).eq("id", campaign_id).execute()
            
            if not response.data:
                raise RuntimeError(f"Campaign {campaign_id} not found")
            
            return response.data[0]
            
        except Exception as e:
            raise RuntimeError(f"Database error saving Subconscious results: {str(e)}")
    
    
    def save_openai_results(
        self,
        campaign_id: int,
        prompt: str,
        response_content: str,
        tokens_used: Dict[str, int],
        cost_usd: float,
        duration_seconds: float
    ) -> Dict[str, Any]:
        """
        Save OpenAI API request and response.
        
        Args:
            campaign_id: Campaign ID
            prompt: Prompt sent to OpenAI
            response_content: Response from OpenAI
            tokens_used: Token usage stats
            cost_usd: API call cost
            duration_seconds: Generation duration
            
        Returns:
            Updated campaign record
        """
        try:
            update_data = {
                "openai_request": {"prompt": prompt},
                "openai_response": {"content": response_content, "tokens": tokens_used},
                "generation_duration_seconds": duration_seconds,
                "api_costs": {"openai_usd": cost_usd},
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = self.client.table("campaigns").update(update_data).eq("id", campaign_id).execute()
            
            if not response.data:
                raise RuntimeError(f"Campaign {campaign_id} not found")
            
            return response.data[0]
            
        except Exception as e:
            raise RuntimeError(f"Database error saving OpenAI results: {str(e)}")
    
    
    def save_generated_emails(
        self,
        campaign_id: int,
        emails: List[Dict[str, Any]],
        campaign_strategy: str
    ) -> List[Dict[str, Any]]:
        """
        Save generated emails to database.
        
        Args:
            campaign_id: Campaign ID
            emails: List of email objects
            campaign_strategy: Overall campaign strategy
            
        Returns:
            List of created email records
        """
        try:
            # Prepare email records
            email_records = [
                {
                    "campaign_id": campaign_id,
                    "email_number": email["email_number"],
                    "subject_line": email["subject_line"],
                    "email_body": email["email_body"],
                    "cta_text": email["cta_text"],
                    "target_mindset": email.get("target_mindset"),
                    "key_insight_used": email.get("key_insight_used")
                }
                for email in emails
            ]
            
            # Insert emails
            response = self.client.table("generated_emails").insert(email_records).execute()
            
            if not response.data:
                raise RuntimeError("Failed to save emails")
            
            # Update campaign with strategy and completion status
            self.client.table("campaigns").update({
                "status": "completed",
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", campaign_id).execute()
            
            return response.data
            
        except Exception as e:
            raise RuntimeError(f"Database error saving emails: {str(e)}")
    
    
    def get_campaign(self, campaign_id: int) -> Optional[Dict[str, Any]]:
        """
        Get campaign by ID with associated emails.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Campaign record with emails, or None if not found
        """
        try:
            # Get campaign
            response = self.client.table("campaigns").select("*").eq("id", campaign_id).execute()
            
            if not response.data:
                return None
            
            campaign = response.data[0]
            
            # Get associated emails
            emails_response = self.client.table("generated_emails").select("*").eq("campaign_id", campaign_id).order("email_number").execute()
            
            campaign["generated_emails"] = emails_response.data if emails_response.data else []
            
            return campaign
            
        except Exception as e:
            raise RuntimeError(f"Database error getting campaign: {str(e)}")
    
    
    def list_recent_campaigns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent campaigns.
        
        Args:
            limit: Maximum number of campaigns to return
            
        Returns:
            List of campaign records
        """
        try:
            response = self.client.table("campaigns").select("*").order("created_at", desc=True).limit(limit).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            raise RuntimeError(f"Database error listing campaigns: {str(e)}")


# Convenience functions for the main API
def save_complete_campaign(
    product_description: str,
    target_audience_urls: List[str],
    subconscious_data: Dict[str, Any],
    openai_prompt: str,
    openai_response: str,
    openai_tokens: Dict[str, int],
    openai_cost: float,
    emails: List[Dict[str, Any]],
    campaign_strategy: str,
    duration_seconds: float
) -> Dict[str, Any]:
    """
    Complete workflow: create campaign, save all data, return final result.
    
    Returns:
        Complete campaign record with all associated data
    """
    db = SupabaseClient()
    
    try:
        # 1. Create campaign
        campaign = db.create_campaign(product_description, target_audience_urls)
        campaign_id = campaign["id"]
        
        # 2. Update to processing status
        db.update_campaign_status(campaign_id, "processing")
        
        # 3. Save Subconscious results
        db.save_subconscious_results(
            campaign_id=campaign_id,
            experiment_id=subconscious_data.get("experiment_id", "mock"),
            request_payload={"product_description": product_description, "audience_urls": target_audience_urls},
            response_data=subconscious_data
        )
        
        # 4. Save OpenAI results
        db.save_openai_results(
            campaign_id=campaign_id,
            prompt=openai_prompt,
            response_content=openai_response,
            tokens_used=openai_tokens,
            cost_usd=openai_cost,
            duration_seconds=duration_seconds
        )
        
        # 5. Save generated emails
        db.save_generated_emails(
            campaign_id=campaign_id,
            emails=emails,
            campaign_strategy=campaign_strategy
        )
        
        # 6. Get complete record
        return db.get_campaign(campaign_id)
        
    except Exception as e:
        # Mark as failed
        try:
            db.update_campaign_status(campaign_id, "failed", str(e))
        except:
            pass
        raise


# Testing
if __name__ == "__main__":
    print("=== TESTING SUPABASE INTEGRATION ===\n")
    
    # Check for credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("⚠ SUPABASE_URL and SUPABASE_KEY not set - skipping live test")
        print("  Set your credentials in .env to test real database operations\n")
        print("Mock flow (what happens when credentials are set):")
        print("  1. Create campaign record (status: pending)")
        print("  2. Update status to 'processing'")
        print("  3. Save Subconscious API results")
        print("  4. Save OpenAI API results")
        print("  5. Save generated emails")
        print("  6. Update status to 'completed'")
        print("  7. Retrieve complete campaign record\n")
    else:
        try:
            db = SupabaseClient()
            
            print("1. Creating test campaign...")
            campaign = db.create_campaign(
                product_description="Test product",
                target_audience_urls=["https://linkedin.com/in/test"]
            )
            print(f"   ✓ Created campaign ID: {campaign['id']}\n")
            
            print("2. Listing recent campaigns...")
            recent = db.list_recent_campaigns(limit=5)
            print(f"   ✓ Found {len(recent)} recent campaigns\n")
            
            print("=== TEST COMPLETE ===")
            print(f"Note: Created test campaign ID {campaign['id']}")
            print("You can delete it manually or let it stay for testing\n")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
            print("Make sure you've run setup_database.sql in your Supabase instance first!\n")

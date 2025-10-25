"""
OpenAI Integration Module

Handles all interactions with OpenAI GPT-4 API for campaign generation.
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenAIClient:
    """Wrapper for OpenAI API calls."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo-preview"  # Use latest GPT-4 Turbo
        
    
    def generate_campaign(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 3000
    ) -> Dict[str, Any]:
        """
        Generate email campaign using GPT-4.
        
        Args:
            prompt: The detailed prompt for campaign generation
            temperature: Creativity level (0.0-1.0, default 0.7)
            max_tokens: Maximum response length
            
        Returns:
            Dict with 'content', 'tokens_used', and 'model' keys
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert B2B email copywriter with deep expertise in "
                            "behavioral psychology and data-driven marketing. You write "
                            "compelling, conversion-focused email campaigns based on "
                            "behavioral research insights. Always return valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            # Extract response content
            content = response.choices[0].message.content
            
            # Calculate token usage and cost
            tokens_used = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            # GPT-4 Turbo pricing (as of 2024)
            cost = self._calculate_cost(
                prompt_tokens=tokens_used["prompt_tokens"],
                completion_tokens=tokens_used["completion_tokens"]
            )
            
            return {
                "content": content,
                "tokens_used": tokens_used,
                "model": response.model,
                "cost_usd": cost,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")
    
    
    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate cost based on GPT-4 Turbo pricing.
        
        Current rates (as of 2024):
        - Input: $0.01 per 1K tokens
        - Output: $0.03 per 1K tokens
        """
        input_cost = (prompt_tokens / 1000) * 0.01
        output_cost = (completion_tokens / 1000) * 0.03
        return round(input_cost + output_cost, 4)


# Convenience function for quick testing
async def generate_email_campaign(
    prompt: str,
    api_key: Optional[str] = None,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Generate an email campaign from a prompt.
    
    Args:
        prompt: Campaign generation prompt
        api_key: OpenAI API key (optional)
        temperature: Creativity level
        
    Returns:
        OpenAI response with campaign content
    """
    client = OpenAIClient(api_key=api_key)
    return client.generate_campaign(prompt, temperature=temperature)


# Testing
if __name__ == "__main__":
    import asyncio
    from reasoning_layer import build_openai_prompt, summarize_results
    from mock_subconscious import get_sample_mock_response
    
    async def test_openai_integration():
        print("=== TESTING OPENAI INTEGRATION ===\n")
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠ OPENAI_API_KEY not set - skipping live test")
            print("  Set your API key in .env to test real OpenAI calls\n")
            
            # Show what would happen
            print("Mock flow (what happens when API key is set):")
            print("  1. Get behavioral insights from Subconscious")
            print("  2. Summarize insights")
            print("  3. Build detailed prompt")
            print("  4. Call OpenAI GPT-4")
            print("  5. Parse JSON response")
            print("  6. Return structured campaign\n")
            return
        
        try:
            # Test with mock Subconscious data
            print("1. Getting mock Subconscious insights...")
            mock_data = get_sample_mock_response()
            summary = summarize_results(mock_data)
            print(f"   ✓ Summarized {len(summary['mindset_breakdown'])} mindsets\n")
            
            # Build prompt
            print("2. Building OpenAI prompt...")
            prompt = build_openai_prompt(
                product_description="AI-powered email marketing automation for B2B SaaS companies",
                summary=summary,
                num_emails=3
            )
            print(f"   ✓ Generated prompt ({len(prompt)} chars)\n")
            
            # Call OpenAI
            print("3. Calling OpenAI GPT-4 (this may take 10-30 seconds)...")
            result = await generate_email_campaign(prompt, temperature=0.7)
            
            print(f"   ✓ Generated campaign!")
            print(f"   ✓ Tokens used: {result['tokens_used']['total_tokens']}")
            print(f"   ✓ Cost: ${result['cost_usd']}")
            print(f"   ✓ Model: {result['model']}\n")
            
            # Parse response
            print("4. Campaign preview:")
            import json
            campaign_data = json.loads(result['content'])
            emails = campaign_data.get('emails', [])
            print(f"   ✓ Generated {len(emails)} emails")
            
            if emails:
                print(f"\n   Email 1 Preview:")
                print(f"   Subject: {emails[0].get('subject_line', 'N/A')}")
                print(f"   Target: {emails[0].get('target_mindset', 'N/A')}")
                print(f"   Body: {emails[0].get('email_body', '')[:100]}...\n")
            
            print("=== TEST COMPLETE ===")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
    
    # Run test
    asyncio.run(test_openai_integration())

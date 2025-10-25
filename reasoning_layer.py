"""
Reasoning Layer - Extract Insights and Build Prompts

This module processes Subconscious API results and constructs intelligent
prompts for the OpenAI GPT-4 model to generate personalized email campaigns.
"""

from typing import Dict, Any, List, Tuple


def summarize_results(subconscious_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract key insights from Subconscious API response.
    
    Args:
        subconscious_response: Full response from Subconscious API (or mock)
        
    Returns:
        Structured summary with actionable insights
    """
    
    insights = subconscious_response.get("insights", {})
    mindset_segments = subconscious_response.get("mindset_segments", [])
    amce_results = subconscious_response.get("amce_results", [])
    wtp_data = subconscious_response.get("willingness_to_pay", {})
    
    # Extract winning messaging angle and top attributes
    winning_angle = insights.get("winning_messaging_angle", "Value & ROI")
    top_attribute = insights.get("top_performing_attribute", "")
    
    # Get mindset breakdown
    mindset_breakdown = [
        {
            "name": segment["name"],
            "percentage": segment["percentage"],
            "characteristics": segment["characteristics"]
        }
        for segment in mindset_segments
    ]
    
    # Sort by percentage descending
    mindset_breakdown.sort(key=lambda x: x["percentage"], reverse=True)
    
    # Extract top performing messages per mindset
    segment_recommendations = insights.get("segment_recommendations", [])
    
    # Calculate overall engagement drivers
    engagement_drivers = _extract_top_drivers(amce_results)
    
    # Build structured summary
    summary = {
        "winning_insight": insights.get("summary", ""),
        "top_messaging_angle": winning_angle,
        "top_performing_attribute": top_attribute,
        
        "mindset_breakdown": mindset_breakdown,
        "largest_segment": mindset_breakdown[0] if mindset_breakdown else None,
        
        "segment_recommendations": segment_recommendations,
        "engagement_drivers": engagement_drivers,
        
        "experiment_metadata": {
            "experiment_id": subconscious_response.get("experiment_id"),
            "sample_size": subconscious_response.get("sample_size"),
            "confidence_level": subconscious_response.get("confidence_level")
        }
    }
    
    return summary


def _extract_top_drivers(amce_results: List[Dict]) -> List[Dict]:
    """Extract top engagement drivers across all mindsets."""
    
    if not amce_results:
        return []
    
    # Aggregate AMCE scores across mindsets
    all_effects = []
    for mindset_data in amce_results:
        for effect in mindset_data.get("effects", []):
            all_effects.append({
                "attribute": effect["attribute"],
                "level": effect["level"],
                "amce": effect["amce"],
                "mindset": mindset_data["mindset"]
            })
    
    # Sort by AMCE score (highest = strongest positive effect)
    all_effects.sort(key=lambda x: x["amce"], reverse=True)
    
    # Return top 5 drivers
    return all_effects[:5]


def build_openai_prompt(
    product_description: str,
    summary: Dict[str, Any],
    num_emails: int = 3
) -> str:
    """
    Build a detailed prompt for OpenAI GPT-4 to generate email campaigns.
    
    Args:
        product_description: The product/service being marketed
        summary: Structured insights from summarize_results()
        num_emails: Number of emails to generate in the sequence
        
    Returns:
        Detailed prompt string for GPT-4
    """
    
    mindset_breakdown = summary["mindset_breakdown"]
    segment_recs = summary.get("segment_recommendations", [])
    winning_angle = summary.get("top_messaging_angle", "")
    winning_insight = summary.get("winning_insight", "")
    
    # Build mindset descriptions
    mindset_descriptions = "\n".join([
        f"- **{m['name']}** ({m['percentage']}%): {m['characteristics']}"
        for m in mindset_breakdown
    ])
    
    # Build segment-specific recommendations
    segment_guidance = "\n\n".join([
        f"**For {rec['mindset']} ({rec['percentage']}%):**\n" +
        "\n".join([f"  - {msg}" for msg in rec.get("key_messages", [])])
        for rec in segment_recs
    ])
    
    # Construct the comprehensive prompt
    prompt = f"""You are an expert B2B email copywriter specializing in behavioral science and personalization.

**YOUR TASK:**
Create a {num_emails}-email campaign sequence for the following product, using insights from behavioral research to maximize engagement and conversion.

**PRODUCT DESCRIPTION:**
{product_description}

**BEHAVIORAL RESEARCH INSIGHTS:**

We conducted a conjoint analysis experiment with your target audience and discovered {len(mindset_breakdown)} distinct behavioral mindsets:

{mindset_descriptions}

**KEY FINDING:**
{winning_insight}

**WINNING MESSAGING ANGLE:** {winning_angle}

**SEGMENT-SPECIFIC RECOMMENDATIONS:**
{segment_guidance}

**EMAIL SEQUENCE REQUIREMENTS:**

Generate exactly {num_emails} emails following this structure:

**Email 1 - Introduction & Hook:**
- Target the largest mindset segment ({mindset_breakdown[0]['name']})
- Lead with the winning messaging angle: "{winning_angle}"
- Create curiosity and establish relevance
- Keep it short (150-200 words)
- Include a soft CTA (e.g., "Learn more", "See how it works")

**Email 2 - Deep Value & Proof:**
- Address the second-largest segment ({mindset_breakdown[1]['name'] if len(mindset_breakdown) > 1 else 'N/A'})
- Provide social proof aligned with their preferences
- Include specific benefits and outcomes
- Length: 200-250 words
- CTA: "Schedule a demo" or "Start free trial"

**Email 3 - Final Push & FOMO:**
- Multi-segment appeal combining top insights
- Create urgency without being pushy
- Overcome final objections
- Strong, clear CTA
- Length: 150-200 words

**FORMATTING REQUIREMENTS:**
- Professional B2B tone (conversational but credible)
- Clear subject lines (under 60 characters)
- Scannable structure with short paragraphs
- Avoid excessive exclamation points
- Each email should stand alone while building on the sequence

**OUTPUT FORMAT:**
Return a valid JSON object with this exact structure:

{{
  "emails": [
    {{
      "email_number": 1,
      "subject_line": "Subject here",
      "email_body": "Full email text here...",
      "cta_text": "CTA button text",
      "target_mindset": "{mindset_breakdown[0]['name']}",
      "key_insight_used": "The specific behavioral insight you emphasized"
    }},
    {{
      "email_number": 2,
      "subject_line": "Subject here",
      "email_body": "Full email text here...",
      "cta_text": "CTA button text",
      "target_mindset": "{mindset_breakdown[1]['name'] if len(mindset_breakdown) > 1 else 'N/A'}",
      "key_insight_used": "The specific behavioral insight you emphasized"
    }},
    {{
      "email_number": 3,
      "subject_line": "Subject here",
      "email_body": "Full email text here...",
      "cta_text": "CTA button text",
      "target_mindset": "Multi-segment",
      "key_insight_used": "The specific behavioral insight you emphasized"
    }}
  ],
  "campaign_strategy": "Brief explanation of the overall campaign strategy and how it leverages the behavioral insights"
}}

Generate the email campaign now:"""

    return prompt


def extract_emails_from_openai_response(openai_response: str) -> Tuple[List[Dict], str]:
    """
    Parse OpenAI response and extract structured email data.
    
    Args:
        openai_response: Raw text response from OpenAI (should be JSON)
        
    Returns:
        Tuple of (emails list, campaign_strategy string)
    """
    import json
    
    try:
        # Try to parse as JSON
        data = json.loads(openai_response)
        
        emails = data.get("emails", [])
        campaign_strategy = data.get("campaign_strategy", "")
        
        # Validate structure
        for email in emails:
            required_fields = ["email_number", "subject_line", "email_body", "cta_text"]
            if not all(field in email for field in required_fields):
                raise ValueError(f"Email missing required fields: {email}")
        
        return emails, campaign_strategy
        
    except json.JSONDecodeError as e:
        # If not valid JSON, try to extract it
        # Look for JSON between triple backticks
        import re
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', openai_response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(1))
            return data.get("emails", []), data.get("campaign_strategy", "")
        
        raise ValueError(f"Could not parse OpenAI response as JSON: {e}")


# Example usage and testing
if __name__ == "__main__":
    from mock_subconscious import get_sample_mock_response
    import json
    
    # Test with mock data
    print("=== TESTING REASONING LAYER ===\n")
    
    # Get mock Subconscious response
    mock_response = get_sample_mock_response()
    
    # Summarize results
    print("1. Summarizing Subconscious results...")
    summary = summarize_results(mock_response)
    print(f"   ✓ Found {len(summary['mindset_breakdown'])} mindset segments")
    print(f"   ✓ Largest segment: {summary['largest_segment']['name']} ({summary['largest_segment']['percentage']}%)")
    print(f"   ✓ Top messaging angle: {summary['top_messaging_angle']}\n")
    
    # Build OpenAI prompt
    print("2. Building OpenAI prompt...")
    prompt = build_openai_prompt(
        product_description="AI-powered email marketing automation for B2B SaaS companies",
        summary=summary,
        num_emails=3
    )
    print(f"   ✓ Generated prompt ({len(prompt)} characters)")
    print(f"   ✓ Preview: {prompt[:200]}...\n")
    
    # Test email extraction with sample response
    print("3. Testing email extraction...")
    sample_openai_response = json.dumps({
        "emails": [
            {
                "email_number": 1,
                "subject_line": "Test Subject",
                "email_body": "Test body",
                "cta_text": "Learn More",
                "target_mindset": "Data-Driven",
                "key_insight_used": "Analytics focus"
            }
        ],
        "campaign_strategy": "Test strategy"
    })
    
    emails, strategy = extract_emails_from_openai_response(sample_openai_response)
    print(f"   ✓ Extracted {len(emails)} email(s)")
    print(f"   ✓ Campaign strategy: {strategy}\n")
    
    print("=== ALL TESTS PASSED ===")

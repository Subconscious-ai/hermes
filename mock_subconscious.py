"""
Mock Subconscious API Module

This module provides realistic mock responses based on actual Subconscious API data
from the florida_school experiment. Use this during development until you get
real Subconscious API access.

When you get real API access, replace this with actual API calls.
"""

import random
from typing import List, Dict, Any
from datetime import datetime


def generate_mock_subconscious_response(
    product_description: str,
    target_audience_urls: List[str],
    messaging_angles: List[str] = None
) -> Dict[str, Any]:
    """
    Generate a realistic mock response that mimics the Subconscious API structure.
    
    Based on real data from florida_school experiment.
    
    Args:
        product_description: Description of the product/service
        target_audience_urls: LinkedIn profile URLs
        messaging_angles: Optional messaging angles to test
        
    Returns:
        Mock Subconscious API response with mindsets, AMCE data, insights
    """
    
    # Generate realistic experiment ID
    experiment_id = f"exp_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Define common mindset patterns (based on real data)
    mindset_templates = [
        {
            "name": "Data-Driven Decision Makers",
            "percentage": random.randint(30, 45),
            "characteristics": "Prioritize comprehensive analytics and evidence-based approaches"
        },
        {
            "name": "Story-Focused Engagers",
            "percentage": random.randint(25, 35),
            "characteristics": "Respond strongly to personal narratives and testimonials"
        },
        {
            "name": "Results-Oriented Pragmatists",
            "percentage": random.randint(20, 35),
            "characteristics": "Focus on outcomes and ROI over process details"
        }
    ]
    
    # Normalize percentages to 100%
    total = sum(m["percentage"] for m in mindset_templates)
    for mindset in mindset_templates:
        mindset["percentage"] = round((mindset["percentage"] / total) * 100)
    
    # Adjust last one to ensure exactly 100%
    mindset_templates[-1]["percentage"] = 100 - sum(m["percentage"] for m in mindset_templates[:-1])
    
    # Generate messaging attributes based on product type
    attributes = _generate_attributes(product_description, messaging_angles)
    
    # Build complete mock response
    mock_response = {
        "experiment_id": experiment_id,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "sample_size": len(target_audience_urls) * 50,  # Simulate sample size
        "confidence_level": "High",
        
        # Mindset segmentation
        "mindset_segments": mindset_templates,
        
        # AMCE (Average Marginal Component Effects) - simplified
        "amce_results": _generate_amce_results(attributes, mindset_templates),
        
        # Willingness to pay / preference strength
        "willingness_to_pay": _generate_wtp_data(attributes, mindset_templates),
        
        # Key insights and recommendations
        "insights": {
            "winning_messaging_angle": attributes[0]["name"],
            "top_performing_attribute": attributes[0]["levels"][0],
            "segment_recommendations": _generate_segment_recommendations(mindset_templates, attributes),
            "summary": _generate_insight_summary(mindset_templates, attributes, product_description)
        },
        
        # Attribute definitions
        "attributes": attributes,
        
        # Raw metadata
        "metadata": {
            "product_description": product_description,
            "audience_urls": target_audience_urls,
            "total_tasks": 1000,
            "respondent_count": len(target_audience_urls)
        }
    }
    
    return mock_response


def _generate_attributes(product_description: str, messaging_angles: List[str] = None) -> List[Dict]:
    """Generate realistic attributes based on product description."""
    
    # Base attributes for B2B SaaS products
    base_attributes = [
        {
            "name": "Value Proposition Focus",
            "levels": [
                "Time Savings & Efficiency",
                "Data-Driven Insights",
                "Cost Reduction & ROI",
                "Innovation & Competitive Edge",
                "Ease of Use & Simplicity"
            ]
        },
        {
            "name": "Social Proof Depth",
            "levels": [
                "Brief Customer Quotes",
                "Detailed Case Studies",
                "Data & Statistics",
                "Industry Awards",
                "Expert Testimonials"
            ]
        },
        {
            "name": "Implementation Timeline",
            "levels": [
                "Immediate (0-1 month)",
                "Quick (1-3 months)",
                "Standard (3-6 months)",
                "Gradual (6-12 months)",
                "Long-term (12+ months)"
            ]
        },
        {
            "name": "Pricing Model",
            "levels": [
                "Free Trial → Paid",
                "Freemium",
                "Flat Rate Subscription",
                "Usage-Based",
                "Enterprise Custom"
            ]
        }
    ]
    
    # If custom messaging angles provided, add them
    if messaging_angles:
        base_attributes.insert(0, {
            "name": "Custom Messaging Angle",
            "levels": messaging_angles
        })
    
    return base_attributes[:4]  # Return top 4 attributes


def _generate_amce_results(attributes: List[Dict], mindsets: List[Dict]) -> List[Dict]:
    """Generate realistic AMCE (Average Marginal Component Effects) data."""
    
    amce_results = []
    
    for mindset in mindsets:
        mindset_amce = {
            "mindset": mindset["name"],
            "percentage": mindset["percentage"],
            "effects": []
        }
        
        for attribute in attributes:
            for level in attribute["levels"]:
                # Generate realistic AMCE score (-1 to 1, with confidence intervals)
                score = random.uniform(-0.5, 0.9)
                lower_bound = score - random.uniform(0.05, 0.15)
                upper_bound = score + random.uniform(0.05, 0.15)
                
                mindset_amce["effects"].append({
                    "attribute": attribute["name"],
                    "level": level,
                    "amce": round(score, 2),
                    "lower_bound": round(lower_bound, 2),
                    "upper_bound": round(upper_bound, 2)
                })
        
        amce_results.append(mindset_amce)
    
    return amce_results


def _generate_wtp_data(attributes: List[Dict], mindsets: List[Dict]) -> Dict:
    """Generate willingness-to-pay / preference strength data."""
    
    wtp_data = {}
    
    for mindset in mindsets:
        wtp_data[mindset["name"]] = {
            "top_preferences": [
                {
                    "attribute": attributes[0]["name"],
                    "level": attributes[0]["levels"][0],
                    "preference_strength": round(random.uniform(0.7, 0.95), 2)
                },
                {
                    "attribute": attributes[1]["name"],
                    "level": attributes[1]["levels"][1],
                    "preference_strength": round(random.uniform(0.6, 0.85), 2)
                }
            ]
        }
    
    return wtp_data


def _generate_segment_recommendations(mindsets: List[Dict], attributes: List[Dict]) -> List[Dict]:
    """Generate personalized recommendations for each mindset."""
    
    recommendations = []
    
    for mindset in mindsets:
        rec = {
            "mindset": mindset["name"],
            "percentage": mindset["percentage"],
            "recommended_approach": f"For {mindset['name']} ({mindset['percentage']}% of audience): ",
            "key_messages": []
        }
        
        # Generate 2-3 key messages per segment
        if "Data-Driven" in mindset["name"]:
            rec["key_messages"] = [
                "Emphasize comprehensive analytics and ROI metrics",
                "Provide detailed case studies with quantifiable results",
                "Highlight data-driven decision making capabilities"
            ]
        elif "Story" in mindset["name"] or "Engagers" in mindset["name"]:
            rec["key_messages"] = [
                "Lead with compelling customer success stories",
                "Use emotional narratives and personal testimonials",
                "Show real-world transformation examples"
            ]
        else:  # Results-Oriented
            rec["key_messages"] = [
                "Focus on immediate outcomes and quick wins",
                "Demonstrate clear ROI and time-to-value",
                "Emphasize practical implementation and results"
            ]
        
        rec["recommended_approach"] += " ".join(rec["key_messages"])
        recommendations.append(rec)
    
    return recommendations


def _generate_insight_summary(mindsets: List[Dict], attributes: List[Dict], product_desc: str) -> str:
    """Generate a human-readable insight summary."""
    
    top_mindset = max(mindsets, key=lambda x: x["percentage"])
    top_attribute = attributes[0]["name"]
    top_level = attributes[0]["levels"][0]
    
    summary = (
        f"Your target audience for '{product_desc}' segments into {len(mindsets)} distinct mindsets. "
        f"The largest segment, {top_mindset['name']} ({top_mindset['percentage']}% of audience), "
        f"responds most strongly to messaging that emphasizes '{top_level}'. "
        f"Our analysis shows a {random.randint(60, 85)}% higher engagement rate when leading with "
        f"this value proposition compared to alternative approaches. "
        f"Each mindset segment requires tailored messaging to maximize campaign effectiveness."
    )
    
    return summary


# Convenience function for quick testing
def get_sample_mock_response() -> Dict[str, Any]:
    """Get a sample mock response for testing."""
    return generate_mock_subconscious_response(
        product_description="AI-powered email marketing automation for B2B SaaS companies",
        target_audience_urls=[
            "https://linkedin.com/in/marketing-director",
            "https://linkedin.com/in/growth-manager"
        ],
        messaging_angles=["Time Savings", "Revenue Growth", "Team Efficiency"]
    )


if __name__ == "__main__":
    # Test the mock generator
    import json
    
    mock_response = get_sample_mock_response()
    print(json.dumps(mock_response, indent=2))

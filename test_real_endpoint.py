"""
Test script for the real /generate-campaign endpoint

This tests the complete Phase 2 workflow:
- Mock Subconscious insights
- Reasoning layer
- OpenAI GPT-4 generation
- Supabase database save (if configured)

Requirements:
- OPENAI_API_KEY in .env (required)
- SUPABASE_URL and SUPABASE_KEY in .env (optional)
"""

import requests
import json
import time

# API endpoint (change if testing deployed version)
BASE_URL = "http://localhost:8000"

# Test payload
payload = {
    "product_description": "AI-powered email marketing automation platform for B2B SaaS companies. Helps marketing teams create, test, and optimize email campaigns using behavioral science and machine learning.",
    "target_audience_urls": [
        "https://linkedin.com/in/marketing-director",
        "https://linkedin.com/in/growth-manager",
        "https://linkedin.com/in/head-of-marketing"
    ],
    "messaging_angles": [
        "Time Savings & Efficiency",
        "Revenue Growth & ROI",
        "Team Productivity"
    ]
}

def test_real_endpoint():
    """Test the real campaign generation endpoint."""
    
    print("=" * 60)
    print("TESTING /generate-campaign ENDPOINT")
    print("=" * 60)
    print()
    
    # Check health first
    print("1. Checking API health...")
    try:
        health = requests.get(f"{BASE_URL}/")
        if health.status_code == 200:
            print(f"   ✅ API is healthy: {health.json()['status']}")
        else:
            print(f"   ❌ API health check failed: {health.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to {BASE_URL}")
        print("   Make sure the server is running: python main.py")
        return
    
    print()
    
    # Call real endpoint
    print("2. Calling /generate-campaign...")
    print(f"   Product: {payload['product_description'][:60]}...")
    print(f"   Audience URLs: {len(payload['target_audience_urls'])} profiles")
    print(f"   Messaging Angles: {len(payload['messaging_angles'])} angles")
    print()
    print("   ⏳ This will take 10-30 seconds (calling OpenAI GPT-4)...")
    print()
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-campaign",
            json=payload,
            timeout=60  # 60 second timeout
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! (took {elapsed:.1f} seconds)")
            print()
            
            # Parse and display result
            result = response.json()
            
            print("=" * 60)
            print("CAMPAIGN GENERATED")
            print("=" * 60)
            print()
            
            print(f"📋 Campaign ID: {result['id']}")
            print(f"📅 Created: {result['created_at']}")
            print()
            
            print("🎯 Winning Insight:")
            print(f"   {result['winning_insight_summary']}")
            print()
            
            print(f"📧 Generated {len(result['generated_campaign'])} Emails:")
            print()
            
            for email in result['generated_campaign']:
                print("-" * 60)
                print(f"EMAIL {email['email_number']}")
                print("-" * 60)
                print(f"Subject: {email['subject']}")
                print(f"CTA: {email['cta']}")
                print()
                print("Body:")
                # Print first 300 chars of body
                body_preview = email['body'][:300]
                if len(email['body']) > 300:
                    body_preview += "..."
                print(body_preview)
                print()
            
            print("=" * 60)
            print("ADDITIONAL DATA")
            print("=" * 60)
            print()
            
            # Show mindset breakdown
            if 'full_subconscious_results' in result:
                mindsets = result['full_subconscious_results'].get('mindset_segments', [])
                if mindsets:
                    print("🧠 Audience Mindset Segments:")
                    for m in mindsets:
                        print(f"   • {m['name']}: {m['percentage']}%")
                        print(f"     {m['characteristics']}")
                    print()
            
            # Show sample size
            if 'full_subconscious_results' in result:
                sample_size = result['full_subconscious_results'].get('sample_size', 'N/A')
                print(f"📊 Sample Size: {sample_size}")
                confidence = result['full_subconscious_results'].get('confidence_level', 'N/A')
                print(f"🎯 Confidence Level: {confidence}")
                print()
            
            print("✅ Test completed successfully!")
            print()
            
            # Option to save full response
            save = input("Save full JSON response to file? (y/n): ").lower().strip()
            if save == 'y':
                filename = f"campaign_result_{int(time.time())}.json"
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"   💾 Saved to {filename}")
            
        elif response.status_code == 400:
            print(f"   ❌ Configuration Error")
            print()
            error = response.json()
            print(f"   {error['detail']}")
            print()
            print("   Make sure you have:")
            print("   1. Created .env file from .env.example")
            print("   2. Added your OPENAI_API_KEY to .env")
            print("   3. Restarted the server")
            
        elif response.status_code == 502:
            print(f"   ❌ External API Error")
            print()
            error = response.json()
            print(f"   {error['detail']}")
            print()
            print("   Check:")
            print("   1. OpenAI API key is valid")
            print("   2. You have billing set up on OpenAI")
            print("   3. You have sufficient credits")
            
        else:
            print(f"   ❌ Unexpected error: {response.status_code}")
            print()
            try:
                print(f"   {response.json()}")
            except:
                print(f"   {response.text}")
    
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timed out after 60 seconds")
        print("   The server might be processing. Try increasing timeout or check logs.")
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
    
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")


def test_mock_endpoint():
    """Quick test of the mock endpoint for comparison."""
    
    print()
    print("=" * 60)
    print("TESTING /generate-campaign-mock ENDPOINT (for comparison)")
    print("=" * 60)
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-campaign-mock",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Mock endpoint working")
            result = response.json()
            print(f"   📧 Returns {len(result['generated_campaign'])} emails")
        else:
            print(f"   ❌ Mock endpoint error: {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()


if __name__ == "__main__":
    # Run tests
    test_real_endpoint()
    test_mock_endpoint()
    
    print()
    print("=" * 60)
    print("Test complete!")
    print("=" * 60)

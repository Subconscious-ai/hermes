"""Quick test of the /generate-campaign endpoint"""
import requests
import json
import time

# Test payload
payload = {
    "product_description": "AI-powered email marketing automation for B2B SaaS companies",
    "target_audience_urls": [
        "https://linkedin.com/in/marketing-director",
        "https://linkedin.com/in/growth-manager"
    ],
    "messaging_angles": ["Time Savings", "Revenue Growth"]
}

print("=" * 60)
print("TESTING /generate-campaign ENDPOINT")
print("=" * 60)
print()
print("⏳ Calling OpenAI GPT-4... (this takes 10-30 seconds)")
print()

start = time.time()

try:
    response = requests.post(
        "http://localhost:8000/generate-campaign",
        json=payload,
        timeout=60
    )
    
    elapsed = time.time() - start
    
    if response.status_code == 200:
        print(f"✅ SUCCESS! (took {elapsed:.1f} seconds)")
        print()
        
        result = response.json()
        
        print(f"Campaign ID: {result['id']}")
        print()
        print(f"Winning Insight:")
        print(f"{result['winning_insight_summary'][:200]}...")
        print()
        print(f"Generated {len(result['generated_campaign'])} emails:")
        print()
        
        for email in result['generated_campaign']:
            print(f"--- EMAIL {email['email_number']} ---")
            print(f"Subject: {email['subject']}")
            print(f"CTA: {email['cta']}")
            print(f"Body preview: {email['body'][:100]}...")
            print()
        
        # Save full result
        with open("campaign_result.json", "w") as f:
            json.dump(result, f, indent=2)
        print("💾 Full result saved to campaign_result.json")
        
    else:
        print(f"❌ Error {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"❌ Error: {e}")

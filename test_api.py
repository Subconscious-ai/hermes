# Quick Test Script for Local API
# Run this to verify your mock endpoint works

import requests
import json

# Test data
test_request = {
    "product_description": "Revolutionary AI-powered marketing automation platform for B2B SaaS companies",
    "target_audience_urls": [
        "https://linkedin.com/in/saas-cmo",
        "https://linkedin.com/in/marketing-vp"
    ],
    "messaging_angles": [
        "time-saving automation",
        "data-driven insights",
        "ROI improvement"
    ]
}

print("🧪 Testing Hermes Campaign Generator API...\n")

# Test 1: Health Check
print("1️⃣ Testing Health Check...")
try:
    response = requests.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 2: Mock Campaign Endpoint
print("2️⃣ Testing Mock Campaign Generation...")
try:
    response = requests.post(
        "http://localhost:8000/generate-campaign-mock",
        json=test_request
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success!")
        print(f"   Campaign ID: {data.get('id')}")
        print(f"   Product: {data.get('product_description')}")
        print(f"   Insight: {data.get('winning_insight_summary')[:100]}...")
        print(f"   Number of Emails: {len(data.get('generated_campaign', []))}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n✅ Testing complete!")

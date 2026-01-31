"""
Sample test cases for AI Scam Detection API
Demonstrates how to test the API with different scenarios
"""

import requests
import json

# API endpoint URL
API_URL = "http://localhost:8000/analyze-call"

# ============================================================================
# TEST CASES
# ============================================================================

def test_safe_call():
    """Test case for a safe call (low risk)"""
    print("\n" + "="*60)
    print("TEST 1: SAFE CALL")
    print("="*60)
    
    payload = {
        "transcript": "Hello, this is John from ABC Bank customer service. I'm calling to confirm your recent transaction.",
        "keyword_score": 10.0,
        "ml_probability": 15.0,
        "voice_stress_score": 5.0
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    print(f"Input: {json.dumps(payload, indent=2)}")
    print(f"\nResponse:")
    print(f"  Final Risk Score: {result['final_risk_score']}")
    print(f"  Risk Label: {result['risk_label']}")
    print(f"  Alert: {result['voice_alert_message']}")


def test_suspicious_call():
    """Test case for a suspicious call (medium risk)"""
    print("\n" + "="*60)
    print("TEST 2: SUSPICIOUS CALL")
    print("="*60)
    
    payload = {
        "transcript": "You need to verify your account immediately. Please provide your card details for security check.",
        "keyword_score": 55.0,
        "ml_probability": 60.0,
        "voice_stress_score": 45.0
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    print(f"Input: {json.dumps(payload, indent=2)}")
    print(f"\nResponse:")
    print(f"  Final Risk Score: {result['final_risk_score']}")
    print(f"  Risk Label: {result['risk_label']}")
    print(f"  Alert: {result['voice_alert_message']}")


def test_scam_call():
    """Test case for a scam call (high risk)"""
    print("\n" + "="*60)
    print("TEST 3: SCAM CALL")
    print("="*60)
    
    payload = {
        "transcript": "URGENT! Your account has been compromised. Wire money immediately to this account or you will lose everything!",
        "keyword_score": 85.0,
        "ml_probability": 95.0,
        "voice_stress_score": 90.0
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    print(f"Input: {json.dumps(payload, indent=2)}")
    print(f"\nResponse:")
    print(f"  Final Risk Score: {result['final_risk_score']}")
    print(f"  Risk Label: {result['risk_label']}")
    print(f"  Alert: {result['voice_alert_message']}")


def test_edge_case_boundary():
    """Test case for boundary values (30 and 70)"""
    print("\n" + "="*60)
    print("TEST 4: BOUNDARY CASE (Score = 30)")
    print("="*60)
    
    payload = {
        "transcript": "This is a test call at the boundary between safe and suspicious.",
        "keyword_score": 30.0,
        "ml_probability": 30.0,
        "voice_stress_score": 30.0
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    print(f"Final Risk Score: {result['final_risk_score']}")
    print(f"Risk Label: {result['risk_label']}")
    print(f"Alert: {result['voice_alert_message']}")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI SCAM DETECTION API - TEST SUITE")
    print("="*60)
    print("\nMake sure the API server is running at http://localhost:8000")
    print("Start server with: uvicorn main:app --reload")
    
    try:
        # Check if API is running
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ API server is running\n")
            
            # Run all test cases
            test_safe_call()
            test_suspicious_call()
            test_scam_call()
            test_edge_case_boundary()
            
            print("\n" + "="*60)
            print("ALL TESTS COMPLETED")
            print("="*60)
        else:
            print("✗ API server responded with error")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API server")
        print("Please start the server with: uvicorn main:app --reload")

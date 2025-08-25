#!/usr/bin/env python3
"""
Test script to verify Grok API integration
"""
import os
import sys
import django

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_support.settings')
django.setup()

from support.grok_integration import generate_grok_response, test_grok_connection

def test_grok_responses():
    """Test Grok API with various customer support scenarios"""
    print("🧪 Testing Grok API Integration...")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "subject": "Technical Issue",
            "message": "My application is not loading properly"
        },
        {
            "subject": "Billing Question", 
            "message": "I was charged twice for my subscription this month"
        },
        {
            "subject": "Feature Request",
            "message": "Can you add dark mode to the mobile app?"
        },
        {
            "subject": "Login Problem",
            "message": "I forgot my password and can't reset it"
        }
    ]
    
    print("🔗 Testing Grok API connection...")
    connection_ok = test_grok_connection()
    
    if not connection_ok:
        print("❌ Cannot proceed with testing - API connection failed")
        print("💡 Make sure GROK_API_KEY is set in your environment variables")
        return False
    
    print("✅ Connection successful! Testing responses...")
    print("-" * 50)
    
    all_success = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['subject']}")
        print(f"💬 Message: {test_case['message']}")
        
        try:
            response = generate_grok_response(test_case['subject'], test_case['message'])
            print(f"🤖 Response: {response}")
            print(f"📏 Length: {len(response)} characters")
            
            if "error" in response.lower():
                print(f"❌ Error in response: {response}")
                all_success = False
            else:
                print("✅ Response generated successfully")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            all_success = False
    
    return all_success

if __name__ == "__main__":
    success = test_grok_responses()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 All Grok API tests passed!")
        print("\n💡 The Grok integration is ready to use in your customer support application.")
    else:
        print("\n❌ Some tests failed. Please check your API key and network connection.")

import os
import requests
import json
from django.conf import settings

def generate_grok_response(subject, message):
    """
    Generate AI response using Grok API (Llama model)
    
    Args:
        subject (str): Ticket subject
        message (str): Customer message
    
    Returns:
        str: AI-generated response or error message
    """
    try:
        # Get API key from environment or settings
        api_key = os.getenv('GROK_API_KEY') or getattr(settings, 'GROK_API_KEY', None)
        
        if not api_key:
            return "Grok API key not configured. Please set GROK_API_KEY in environment variables."
        
        # Grok API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Create prompt for customer support
        prompt = f"""
        As a customer support agent, please provide a professional and helpful response to the following customer query.
        
        IMPORTANT: Your response MUST be under 255 characters total and focus on being concise yet helpful.
        
        Ticket Subject: {subject}
        Customer Message: {message}
        
        Provide a solution-oriented response that addresses the customer's concern while maintaining a professional and empathetic tone.
        """
        
        # Request payload
        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful customer support assistant. Provide concise, professional responses that solve customer problems efficiently."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,  # Limit response length
            "temperature": 0.7
        }
        
        # Make API request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        ai_response = result['choices'][0]['message']['content'].strip()
        
        # Ensure response is within character limit
        if len(ai_response) > 255:
            ai_response = ai_response[:247] + "..."
            
        return ai_response
        
    except requests.exceptions.RequestException as e:
        print(f"Grok API Request Error: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_data = e.response.json()
                return f"API Error: {error_data.get('error', {}).get('message', str(e))}"
            except:
                return f"API Error: {e.response.text}"
        return "Network error occurred while connecting to Grok API."
    
    except Exception as e:
        print(f"Grok Integration Error: {e}")
        return "An unexpected error occurred while generating the AI response."

def test_grok_connection():
    """
    Test the Grok API connection
    Returns True if successful, False otherwise
    """
    try:
        api_key = os.getenv('GROK_API_KEY') or getattr(settings, 'GROK_API_KEY', None)
        if not api_key:
            print("GROK_API_KEY not found")
            return False
            
        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("Grok API connection successful")
        models = response.json().get('data', [])
        print(f"Available models: {len(models)}")
        return True
        
    except Exception as e:
        print(f"Grok API connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    if test_grok_connection():
        # Test a sample response
        test_subject = "Technical Support"
        test_message = "My application keeps crashing when I try to upload files"
        
        print(f"\nTesting Grok response generation...")
        response = generate_grok_response(test_subject, test_message)
        print(f"Test Subject: {test_subject}")
        print(f"Test Message: {test_message}")
        print(f"AI Response: {response}")
        print(f"Length: {len(response)} characters")

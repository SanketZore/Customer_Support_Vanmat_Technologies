import os
import google.generativeai as genai
from django.conf import settings
import time

def configure_gemini():
    """Configure Gemini API with the API key"""
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai

def generate_ai_response(subject, message, model_type='flash'):
    """
    Generate AI response using Google Gemini API with model selection
    
    Args:
        subject (str): Ticket subject
        message (str): Customer message
        model_type (str): 'pro' for Gemini 1.5 Pro, 'flash' for Gemini 1.5 Flash
    
    Returns:
        str: AI-generated response
    """
    try:
        # Configure Gemini API
        genai = configure_gemini()
        
        # Select model based on type
        if model_type.lower() == 'pro':
            model_name = 'gemini-1.5-pro-latest'
            char_limit = 500  # Pro can handle longer responses
        else:
            model_name = 'gemini-1.5-flash-latest'
            char_limit = 250 
        
        # Create model instance
        model = genai.GenerativeModel(model_name)
        
        # Create prompt optimized for the selected model
        prompt = f"""
        As a customer support agent, please provide a professional and helpful response to the following customer query.
        
        IMPORTANT: Your response MUST be under {char_limit} characters total.
        
        Ticket Subject: {subject}
        Customer Message: {message}
        
        Provide a concise, empathetic, and solution-oriented response. 
        Keep it professional, customer-friendly, and within the character limit.
        Focus on the most important information and solutions.
        """
        
        # Generate response with timing
        start_time = time.time()
        response = model.generate_content(prompt)
        response_time = time.time() - start_time
        
        # Log performance (optional - can be removed in production)
        print(f"{model_name.upper()} Response generated in {response_time:.2f}s")
        print(f"Response length: {len(response.text)} characters")
        
        return response.text
        
    except Exception as e:
        # Log the error for debugging
        print(f"Gemini API Error ({model_type}): {e}")
        
        # Provide a clear message regarding quota issues
        if "quota" in str(e).lower():
            return "The AI response generation limit has been exceeded. Please try again later or check your API usage."
        elif "model" in str(e).lower() and "not found" in str(e).lower():
            # Fallback to default model if specified model is not available
            if model_type != 'flash':
                return generate_ai_response(subject, message, 'flash')
            return "The AI model is currently unavailable. Please try again later."
        else:
            return "An error occurred while generating the AI response. Please try again."

def compare_models(subject, message):
    """
    Compare responses from both Pro and Flash models
    
    Returns:
        dict: Responses and performance metrics from both models
    """
    results = {}
    
    # Test Pro model
    start_time = time.time()
    pro_response = generate_ai_response(subject, message, 'pro')
    pro_time = time.time() - start_time
    
    # Test Flash model  
    start_time = time.time()
    flash_response = generate_ai_response(subject, message, 'flash')
    flash_time = time.time() - start_time
    
    results['pro'] = {
        'response': pro_response,
        'response_time': pro_time,
        'length': len(pro_response)
    }
    
    results['flash'] = {
        'response': flash_response,
        'response_time': flash_time,
        'length': len(flash_response)
    }
    
    results['time_difference'] = pro_time - flash_time
    results['time_ratio'] = pro_time / flash_time if flash_time > 0 else float('inf')
    
    return results

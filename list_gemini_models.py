#!/usr/bin/env python3
"""
Script to list available Gemini models
"""
import os
import sys
import django

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customer_support.settings')
django.setup()

import google.generativeai as genai
from django.conf import settings

def list_available_models():
    """List all available Gemini models"""
    print("Listing available Gemini models...")
    
    try:
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # List available models
        models = genai.list_models()
        
        print("Available models:")
        for model in models:
            print(f"  - {model.name}")
            print(f"    Supported methods: {model.supported_generation_methods}")
            print()
            
        return True
    except Exception as e:
        print(f"Error listing models: {e}")
        return False

if __name__ == "__main__":
    success = list_available_models()
    if success:
        print("Model listing completed successfully!")
    else:
        print("Failed to list models!")

import os
from support.grok_integration import generate_grok_response

def main():
    # Load environment variables
    api_key = os.getenv('GROK_API_KEY')
    if not api_key:
        print("GROK_API_KEY not found. Please set it in your environment variables.")
        return

    # Example subject and message
    subject = "Technical Support"
    message = "My application keeps crashing when I try to upload files"

    # Generate response
    response = generate_grok_response(subject, message)
    print(f"AI Response: {response}")

if __name__ == "__main__":
    main()



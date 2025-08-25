# Grok API Integration Guide

## Overview
This guide explains how to integrate the Grok API (using Llama models) for AI-generated customer support responses in your Django application.

## Step 1: Get Grok API Key

1. **Visit Groq Console**: Go to [https://console.groq.com/](https://console.groq.com/)

2. **Sign up/Login**: Create an account or sign in with your existing credentials

3. **Create API Key**:
   - Navigate to API Keys section
   - Click "Create API Key"
   - Give your key a descriptive name (e.g., "Customer Support AI")
   - Copy the generated API key

## Step 2: Set Up Environment Variables

Add your Grok API key to your `.env` file:

```env
GROK_API_KEY=gsk_your_actual_api_key_here
```

## Step 3: Integration Files

### Main Integration File: `support/grok_integration.py`
- `generate_grok_response(subject, message)`: Main function to generate AI responses
- `test_grok_connection()`: Function to test API connectivity

### Updated View: `support/views.py`
- Modified `generate_ai_reply()` function to use Grok instead of Gemini

## Step 4: API Configuration

The integration uses the following configuration:
- **Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Response Limit**: 250 characters maximum
- **Temperature**: 0.7 (balanced creativity)

## Step 5: Testing the Integration

Run the test script to verify everything works:

```bash
python test_grok_integration.py
```

## Step 6: Usage in Application

The AI response generation is automatically integrated into the admin dashboard. When staff users view tickets, they can:

1. Click "Generate AI Reply" button
2. The system calls the Grok API with the ticket details
3. The AI-generated response is returned and can be used as-is or modified

## Error Handling

The integration includes comprehensive error handling for:
- Missing API keys
- Network connectivity issues
- API rate limits
- Invalid responses

## Performance Considerations

- **Response Time**: Grok API typically responds in 1-3 seconds
- **Rate Limits**: Be aware of Groq's API rate limits for your plan
- **Caching**: Consider implementing response caching for frequent queries

## Troubleshooting

### Common Issues:

1. **API Key Errors**: Ensure `GROK_API_KEY` is set in your environment
2. **Network Issues**: Check internet connectivity and firewall settings
3. **Rate Limits**: Monitor your API usage in the Groq console
4. **Model Availability**: Verify the specified model is available

### Testing Connectivity:

```python
from support.grok_integration import test_grok_connection
test_grok_connection()
```

## Additional Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [Llama Models Overview](https://llama.meta.com/)
- [Groq Console](https://console.groq.com/)

## Migration from Gemini

If you were previously using Gemini:
1. The `generate_ai_reply()` function now uses Grok
2. Gemini integration files remain available for reference
3. Update your environment variables from `GEMINI_API_KEY` to `GROK_API_KEY`

## Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive data
- Monitor API usage to prevent unexpected charges
- Implement rate limiting in production

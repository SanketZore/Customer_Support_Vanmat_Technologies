
export $(grep -v '^#' .env | xargs)

curl https://api.groq.com/openai/v1/chat/completions -s \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $GROQ_API_KEY" \
-d '{
  "model": "meta-llama/llama-4-scout-17b-16e-instruct",
  "messages": [{
      "role": "user",
      "content": "Explain the importance of fast language models"
  }]
}'

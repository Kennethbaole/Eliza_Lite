import os
import openai

# 1. Setup the Client Once
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# 2. Shared Function
def get_embedding(text):
    # Ensure text is clean
    text = text.replace("\n", " ")
    
    # Call OpenAI
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    
    # Return vector
    return response.data[0].embedding
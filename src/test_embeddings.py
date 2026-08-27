import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What are the shipping delivery times?"
)

embedding = response.embeddings[0].values

print("Embedding generated successfully.")
print("Dimensions:", len(embedding))
print("First 10 values:", embedding[:10])

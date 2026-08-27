import os
import json
import numpy as np

from dotenv import load_dotenv
from google import genai

from chunker import create_chunks


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"

INDEX_FILE = "data/document_index.json"


def get_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def build_index():

    chunks = create_chunks()

    indexed_chunks = []

    total = len(chunks)

    for i, chunk in enumerate(chunks, start=1):

        print(f"Embedding {i}/{total}: {chunk['source']}")

        embedding = get_embedding(chunk["text"])

        indexed_chunks.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding": embedding
        })

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(indexed_chunks, f)

    print()
    print("Index created successfully.")
    print("Chunks indexed:", len(indexed_chunks))
    print("Saved to:", INDEX_FILE)


if __name__ == "__main__":
    build_index()

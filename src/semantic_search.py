import os
import json
import numpy as np

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"
INDEX_FILE = "data/document_index.json"


def load_index():

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_embedding(text):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return np.array(
        response.embeddings[0].values
    )


def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


def search(question, top_k=5):

    index = load_index()

    question_embedding = get_embedding(question)

    scored_results = []

    for item in index:

        document_embedding = np.array(
            item["embedding"]
        )

        score = cosine_similarity(
            question_embedding,
            document_embedding
        )

        scored_results.append({
            "source": item["source"],
            "chunk_id": item["chunk_id"],
            "score": float(score),
            "text": item["text"]
        })

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:top_k]


if __name__ == "__main__":

    question = input("\nEnter a question: ")

    results = search(question)

    print("\n=== SEMANTIC SEARCH RESULTS ===")

    for result in results:

        print("\n" + "=" * 70)
        print("SOURCE:", result["source"])
        print("CHUNK:", result["chunk_id"])
        print("SCORE:", round(result["score"], 4))
        print("\n", result["text"][:1000])

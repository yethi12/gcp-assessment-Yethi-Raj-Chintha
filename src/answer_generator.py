import os

from dotenv import load_dotenv
from google import genai

from semantic_search import search


load_dotenv()


MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

USE_GEMINI = os.getenv(
    "USE_GEMINI",
    "true"
).lower() == "true"


def generate_mock_answer(question, results):

    if not results:
        return (
            "Information not available in the supplied "
            "NorthStar Retail documents."
        )

    best = results[0]

    return (
        "Mock mode: Gemini generation is disabled.\n\n"
        "The most relevant information was retrieved from "
        f"{best['source']}.\n\n"
        f"Retrieved information:\n{best['text'][:1500]}\n\n"
        f"Source: {best['source']}"
    )


def generate_answer(question):

    results = search(
        question,
        top_k=3
    )

    MIN_SIMILARITY = 0.45

    if (
        not results
        or results[0]["score"] < MIN_SIMILARITY
    ):
        return (
            "I could not find sufficient information "
            "in the supplied NorthStar Retail documents "
            "to answer this question."
        )

    # ------------------------------------------------
    # MOCK MODE
    # ------------------------------------------------

    if not USE_GEMINI:

        return generate_mock_answer(
            question,
            results
        )

    # ------------------------------------------------
    # GEMINI MODE
    # ------------------------------------------------

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return (
            "Gemini credentials are not configured. "
            "Please set GOOGLE_API_KEY or use "
            "USE_GEMINI=false for mock mode."
        )

    client = genai.Client(
        api_key=api_key
    )

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
SOURCE: {result['source']}
CHUNK: {result['chunk_id']}

{result['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are the NorthStar Retail support assistant.

Answer the user's question using ONLY the
supplied document context.

Do not use outside knowledge.

If the context does not contain enough information
to answer the question, say that the information
is not available in the supplied documents.

Keep the answer concise and factual.

Always identify the source document used.

USER QUESTION:
{question}

DOCUMENT CONTEXT:
{context}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    question = input(
        "\nEnter a question: "
    )

    answer = generate_answer(
        question
    )

    print("\n=== ANSWER ===")
    print(answer)

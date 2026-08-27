import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


SALES_KEYWORDS = [
    "sales",
    "sale",
    "revenue",
    "sold",
    "selling",
    "category",
    "categories",
    "region",
    "regions",
    "geographical",
    "geographic",
    "area",
    "best selling",
    "top selling",
    "highest revenue",
    "lowest revenue",
    "most sold",
    "sales performance",
]


POLICY_KEYWORDS = [
    "return",
    "returns",
    "send back",
    "refund",
    "refunds",
    "warranty",
    "shipping",
    "delivery",
    "promotion",
    "promotions",
    "discount",
    "loyalty",
    "points",
    "support",
    "size",
    "sizing",
    "exchange",
]


def keyword_classify(question):

    text = question.lower().strip()

    sales_score = sum(
        1 for keyword in SALES_KEYWORDS
        if keyword in text
    )

    policy_score = sum(
        1 for keyword in POLICY_KEYWORDS
        if keyword in text
    )

    if sales_score > policy_score:
        return "SALES"

    if policy_score > sales_score:
        return "POLICY"

    return None


def gemini_classify(question):

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "POLICY"

    client = genai.Client(api_key=api_key)

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash"
    )

    prompt = f"""
Classify the following NorthStar Retail customer
question into exactly one category:

SALES
POLICY

SALES means questions about:
- sales
- revenue
- products sold
- categories
- regions
- orders
- sales performance

POLICY means questions about:
- returns
- refunds
- warranty
- shipping
- delivery
- promotions
- loyalty
- customer support
- sizing

Return ONLY one word:
SALES or POLICY

Question:
{question}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    result = response.text.strip().upper()

    if "SALES" in result:
        return "SALES"

    return "POLICY"


def classify_question(question):

    route = keyword_classify(question)

    if route is not None:
        return route

    return gemini_classify(question)


if __name__ == "__main__":

    while True:

        question = input(
            "\nEnter a question (or 'exit'): "
        )

        if question.lower().strip() == "exit":
            break

        route = classify_question(question)

        print("Route:", route)

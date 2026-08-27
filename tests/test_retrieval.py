from src.semantic_search import search


def test_shipping_question_retrieves_shipping_document():

    results = search(
        "What are the shipping delivery times?",
        top_k=3
    )

    assert len(results) > 0

    sources = [
        result["source"]
        for result in results
    ]

    assert "shipping.json" in sources


def test_return_question_retrieves_return_document():

    results = search(
        "What is the return policy?",
        top_k=3
    )

    assert len(results) > 0

    sources = [
        result["source"]
        for result in results
    ]

    assert "returns.pdf" in sources

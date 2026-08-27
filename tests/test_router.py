from src.router import classify_question


def test_revenue_question_routes_to_sales():

    question = "What is the revenue by region?"

    assert classify_question(question) == "SALES"


def test_product_sales_question_routes_to_sales():

    question = "Which products generated the most revenue?"

    assert classify_question(question) == "SALES"


def test_shipping_question_routes_to_policy():

    question = "What are the shipping delivery times?"

    assert classify_question(question) == "POLICY"


def test_return_question_routes_to_policy():

    question = "What is the return policy?"

    assert classify_question(question) == "POLICY"


def test_ambiguous_refund_question_routes_to_policy():

    question = "Can I get my money back for an item?"

    assert classify_question(question) == "POLICY"

from router import classify_question
from sales_queries import get_sales_answer
from answer_generator import generate_answer


def answer_question(question):

    route = classify_question(question)

    print(f"\nRoute selected: {route}")

    if route == "SALES":
        return get_sales_answer(question)

    elif route == "POLICY":
        return generate_answer(question)

    else:
        return "Sorry, I could not determine how to answer that question."


def main():

    print("=" * 60)
    print("NorthStar Retail Assistant")
    print("=" * 60)

    print("\nAsk a sales or policy question.")
    print("Type 'exit' to quit.")

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = answer_question(question)

            print("\n=== ANSWER ===")
            print(answer)

        except Exception as e:
            print("\nAn error occurred:")
            print(str(e))


if __name__ == "__main__":
    main()

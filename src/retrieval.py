from chunker import create_chunks

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentRetriever:

    def __init__(self):

        self.chunks = create_chunks()

        # Include source filename in searchable text.
        searchable_text = [
            f"{chunk['source']} {chunk['text']}"
            for chunk in self.chunks
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.document_vectors = self.vectorizer.fit_transform(
            searchable_text
        )

    def search(self, question, top_k=3):

        question_vector = self.vectorizer.transform([question])

        scores = cosine_similarity(
            question_vector,
            self.document_vectors
        )[0]

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            results.append({
                "source": self.chunks[index]["source"],
                "chunk_id": self.chunks[index]["chunk_id"],
                "score": float(scores[index]),
                "text": self.chunks[index]["text"]
            })

        return results


if __name__ == "__main__":

    retriever = DocumentRetriever()

    question = input("\nEnter a question: ")

    results = retriever.search(question)

    print("\n=== SEARCH RESULTS ===")

    for result in results:

        print("\n" + "=" * 60)
        print("SOURCE:", result["source"])
        print("CHUNK:", result["chunk_id"])
        print("SCORE:", round(result["score"], 4))
        print("\n", result["text"][:1000])

from document_loader import load_all_documents


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks():

    documents = load_all_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "source": document["source"],
                "chunk_id": index,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print("Documents processed:", 8)
    print("Total chunks:", len(chunks))

    print("\nFirst 5 chunks:\n")

    for chunk in chunks[:5]:

        print("=" * 60)
        print("SOURCE:", chunk["source"])
        print("CHUNK:", chunk["chunk_id"])
        print(chunk["text"][:500])

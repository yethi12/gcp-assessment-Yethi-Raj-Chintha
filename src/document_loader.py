from pathlib import Path
import json
import pandas as pd
from pypdf import PdfReader


DOCUMENT_DIR = Path("data/product_docs")


def load_pdf(path):
    reader = PdfReader(path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_txt(path):
    return path.read_text(encoding="utf-8")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert JSON structure into readable text
    return json.dumps(data, indent=2, ensure_ascii=False)


def load_csv(path):
    df = pd.read_csv(path)

    # Convert every row into readable text
    return df.to_string(index=False)


def load_document(path):
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = load_pdf(path)

    elif suffix == ".txt":
        text = load_txt(path)

    elif suffix == ".json":
        text = load_json(path)

    elif suffix == ".csv":
        text = load_csv(path)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return {
        "source": path.name,
        "text": text,
    }


def load_all_documents():
    documents = []

    for path in sorted(DOCUMENT_DIR.iterdir()):

        if not path.is_file():
            continue

        document = load_document(path)

        documents.append(document)

    return documents


if __name__ == "__main__":

    documents = load_all_documents()

    print("Documents loaded:", len(documents))

    for document in documents:
        print("\n" + "=" * 60)
        print("SOURCE:", document["source"])
        print("TEXT LENGTH:", len(document["text"]))
        print("PREVIEW:")
        print(document["text"][:500])

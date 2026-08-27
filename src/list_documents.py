from pathlib import Path


DOCUMENT_DIR = Path("data/product_docs")


if __name__ == "__main__":

    print("Documents found:\n")

    for file in sorted(DOCUMENT_DIR.iterdir()):
        if file.is_file():
            print(f"{file.name}  |  {file.suffix}")

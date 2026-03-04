"""
Update all existing ChromaDB verse embeddings with embedding_type='single_verse'.

Iterates through the collection in batches and adds the new metadata field.
"""

import chromadb
from tqdm import tqdm

CHROMA_PATH = "data/verse_embedding"
COLLECTION_NAME = "bible_verses"
BATCH_SIZE = 5000


def main():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    total = collection.count()
    print(f"Total items in collection: {total:,}")
    print("Updating all items with embedding_type='single_verse'...\n")

    for offset in tqdm(range(0, total, BATCH_SIZE), desc="Batches", unit="batch"):
        batch = collection.get(
            limit=BATCH_SIZE,
            offset=offset,
            include=["metadatas"],
        )

        ids = batch["ids"]
        updated_metadatas = []
        for meta in batch["metadatas"]:
            meta["embedding_type"] = "single_verse"
            updated_metadatas.append(meta)

        collection.update(
            ids=ids,
            metadatas=updated_metadatas,
        )

    print(f"\nDone! Updated {total:,} items with embedding_type='single_verse'.")


if __name__ == "__main__":
    main()

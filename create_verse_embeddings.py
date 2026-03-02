"""
Create a ChromaDB vector database from bible.eng.db verses.

Embeds all verses using google/embeddinggemma-300m and stores them
in a persistent ChromaDB database at data/verse_embedding with metadata:
  - translationId
  - commonName
  - chapterNumber
  - number (verse number)
"""

import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

DB_PATH = "data/bible.eng.db"
CHROMA_PATH = "data/verse_embedding"
COLLECTION_NAME = "bible_verses"
MODEL_NAME = "google/embeddinggemma-300m"
BATCH_SIZE = 4096  # encoding batch size (large — requires ~96GB RAM)
CHROMA_BATCH = 40000  # chromadb insert batch size


def fetch_verses(db_path: str):
    """Fetch all verses with metadata from the SQLite database."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT
            cv.translationId,
            b.commonName,
            cv.chapterNumber,
            cv.number,
            cv.text
        FROM ChapterVerse cv
        JOIN Book b ON cv.bookId = b.id AND cv.translationId = b.translationId
        ORDER BY cv.translationId, b."order", cv.chapterNumber, cv.number
    """
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def main():
    print("Loading verses from database...")
    rows = fetch_verses(DB_PATH)
    total = len(rows)
    print(f"  Found {total:,} verses across translations.\n")

    print(f"Loading embedding model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    print("  Model loaded.\n")

    print(f"Creating ChromaDB at: {CHROMA_PATH}")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    # Delete existing collection if present to start fresh
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"  Collection '{COLLECTION_NAME}' ready.\n")

    # Process in batches
    print("Encoding and inserting verses...")
    for start in tqdm(range(0, total, BATCH_SIZE), desc="Batches", unit="batch"):
        batch_rows = rows[start : start + BATCH_SIZE]

        ids = []
        documents = []
        metadatas = []

        for i, (translation_id, common_name, chapter_num, verse_num, text) in enumerate(batch_rows):
            uid = f"{translation_id}_{common_name}_{chapter_num}_{verse_num}"
            ids.append(uid)
            documents.append(text)
            metadatas.append({
                "translationId": translation_id,
                "commonName": common_name,
                "chapterNumber": int(chapter_num),
                "number": int(verse_num),
            })

        # Encode as documents
        embeddings = model.encode_document(documents)
        embeddings_list = embeddings.tolist()

        # Insert in sub-batches if needed (ChromaDB limits)
        for sub_start in range(0, len(ids), CHROMA_BATCH):
            sub_end = sub_start + CHROMA_BATCH
            collection.add(
                ids=ids[sub_start:sub_end],
                embeddings=embeddings_list[sub_start:sub_end],
                documents=documents[sub_start:sub_end],
                metadatas=metadatas[sub_start:sub_end],
            )

    print(f"\nDone! {collection.count():,} verses stored in {CHROMA_PATH}")


if __name__ == "__main__":
    main()

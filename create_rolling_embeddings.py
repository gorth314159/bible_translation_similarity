"""
Create rolling 5-verse window embeddings and add them to ChromaDB.

For each (translation, book, chapter), concatenates verses in a sliding
window of size 5 (verses 1-5, 2-6, ... (n-4)-n) and embeds the combined
text. Stored with embedding_type='rolling_5_verse' and metadata tracking
the start/end verse numbers.
"""

import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

DB_PATH = "data/bible.eng.db"
CHROMA_PATH = "data/verse_embedding"
COLLECTION_NAME = "bible_verses"
MODEL_NAME = "google/embeddinggemma-300m"
WINDOW_SIZE = 5
BATCH_SIZE = 256  # encoding batch size
CHROMA_BATCH = 5000  # chromadb insert batch size
DEVICE = "cuda"


def fetch_verses(db_path: str):
    """Fetch all verses with metadata, ordered for grouping."""
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


def build_windows(rows):
    """
    Group verses by (translation, book, chapter) and build rolling windows.

    Returns a list of (uid, combined_text, metadata) tuples.
    """
    # Group by (translationId, commonName, chapterNumber)
    chapters = {}
    for translation_id, common_name, chapter_num, verse_num, text in rows:
        key = (translation_id, common_name, chapter_num)
        chapters.setdefault(key, []).append((verse_num, text))

    windows = []
    for (translation_id, common_name, chapter_num), verses in chapters.items():
        # Ensure sorted by verse number
        verses.sort(key=lambda v: v[0])

        if len(verses) < WINDOW_SIZE:
            # Chapter has fewer verses than window size — embed all as one window
            combined = " ".join(text for _, text in verses)
            start_verse = verses[0][0]
            end_verse = verses[-1][0]
            uid = f"{translation_id}_{common_name}_{chapter_num}_v{start_verse}-{end_verse}_r5"
            meta = {
                "translationId": translation_id,
                "commonName": common_name,
                "chapterNumber": int(chapter_num),
                "startVerse": int(start_verse),
                "endVerse": int(end_verse),
                "embedding_type": "rolling_5_verse",
            }
            windows.append((uid, combined, meta))
        else:
            for i in range(len(verses) - WINDOW_SIZE + 1):
                window_verses = verses[i : i + WINDOW_SIZE]
                combined = " ".join(text for _, text in window_verses)
                start_verse = window_verses[0][0]
                end_verse = window_verses[-1][0]
                uid = f"{translation_id}_{common_name}_{chapter_num}_v{start_verse}-{end_verse}_r5"
                meta = {
                    "translationId": translation_id,
                    "commonName": common_name,
                    "chapterNumber": int(chapter_num),
                    "startVerse": int(start_verse),
                    "endVerse": int(end_verse),
                    "embedding_type": "rolling_5_verse",
                }
                windows.append((uid, combined, meta))

    return windows


def main():
    print("Loading verses from database...")
    rows = fetch_verses(DB_PATH)
    print(f"  Found {len(rows):,} verses.\n")

    print("Building rolling 5-verse windows...")
    windows = build_windows(rows)
    total = len(windows)
    print(f"  Created {total:,} windows.\n")

    print(f"Loading embedding model: {MODEL_NAME} on {DEVICE}...")
    model = SentenceTransformer(MODEL_NAME, device=DEVICE)
    print(f"  Model loaded on {model.device}.\n")

    print(f"Opening ChromaDB at: {CHROMA_PATH}")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    existing = collection.count()
    print(f"  Collection '{COLLECTION_NAME}' has {existing:,} existing items.\n")

    print("Encoding and inserting rolling windows...")
    for start in tqdm(range(0, total, BATCH_SIZE), desc="Batches", unit="batch"):
        batch = windows[start : start + BATCH_SIZE]

        ids = [w[0] for w in batch]
        documents = [w[1] for w in batch]
        metadatas = [w[2] for w in batch]

        embeddings = model.encode_document(documents)
        embeddings_list = embeddings.tolist()

        for sub_start in range(0, len(ids), CHROMA_BATCH):
            sub_end = sub_start + CHROMA_BATCH
            collection.add(
                ids=ids[sub_start:sub_end],
                embeddings=embeddings_list[sub_start:sub_end],
                documents=documents[sub_start:sub_end],
                metadatas=metadatas[sub_start:sub_end],
            )

    final = collection.count()
    print(f"\nDone! Collection now has {final:,} items ({final - existing:,} rolling windows added).")


if __name__ == "__main__":
    main()

"""
Run this from your project root (where app/ lives) to check whether
your Chroma document store has duplicate chunks.

    python check_duplicates.py
"""

from app.vectorstores import get_document_db

db = get_document_db()

# Pull everything out of the collection
data = db.get(include=["documents"])
contents = data["documents"]

print(f"Total chunks stored: {len(contents)}")
print(f"Unique chunks:       {len(set(contents))}")

if len(contents) != len(set(contents)):
    dupes = len(contents) - len(set(contents))
    print(f"\n⚠️  Found {dupes} duplicate chunk(s) in the store.")
    print("This is almost certainly why answers repeat content — the same")
    print("passage is being retrieved more than once and stuffed into context.")
else:
    print("\n✅ No duplicates found.")
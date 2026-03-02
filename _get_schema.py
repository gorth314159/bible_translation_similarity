import sqlite3

conn = sqlite3.connect('data/bible.eng.db')
cursor = conn.cursor()

# Get all tables and views
cursor.execute("SELECT type, name, sql FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY type, name")
for row in cursor.fetchall():
    obj_type, name, sql = row
    print(f"--- {obj_type.upper()}: {name} ---")
    print(sql)
    print()

conn.close()

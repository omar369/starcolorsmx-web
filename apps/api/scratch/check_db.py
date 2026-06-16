import sqlite3
import json
import sys
import os

# Set up python path to import app modules
sys.path.append(os.path.abspath("apps/api"))

from app.api.v1.quotes.schemas import QuoteResult

db_path = "apps/api/dev.db"
if not os.path.exists(db_path):
    print(f"Database file {db_path} does not exist!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, customer_name, result_json FROM quotes;")
rows = cursor.fetchall()
print(f"Found {len(rows)} quotes in the local SQLite database:")
for r in rows:
    qid, name, result_str = r
    print(f"\n--- Quote ID: {qid} for {name} ---")
    try:
        result_dict = json.loads(result_str)
        # Try to validate
        validated = QuoteResult.model_validate(result_dict)
        print(f"  Validation SUCCESS: paint={validated.paint_product_name}, price={validated.estimated_price}")
    except Exception as e:
        print(f"  Validation FAILED: {type(e).__name__}: {e}")
        print(f"  JSON content: {result_str}")

conn.close()

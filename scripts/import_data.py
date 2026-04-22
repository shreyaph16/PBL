import os
import pandas as pd
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_pipeline.sentiment_engine import analyze_sentiment
from backend.models.orm_models import Review
from backend.core.config import settings

# Use local sqlite by default if not in docker, or allow env override
DB_URL = os.getenv("DATABASE_URL") or "sqlite:///./sentiment.db"
CSV_FILE = "laptops_dataset_final_600.csv"

def seed_database():
    print(f"[*] Starting migration from {CSV_FILE}")
    
    if not os.path.exists(CSV_FILE):
        print(f"[!] Error: {CSV_FILE} not found in root directory.")
        return

    # Load data
    df = pd.read_csv(CSV_FILE)
    print(f"[*] Loaded {len(df)} rows. Analyzing sentiment for first 50 records...")

    # Setup DB
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    count = 0
    # We'll analysis-seed the first 50 to avoid long wait times during setup
    for _, row in df.head(50).iterrows():
        review_text = str(row['review'])
        if not review_text or review_text.strip() == "":
            continue
            
        try:
            # Perform analysis
            result = analyze_sentiment(review_text)
            
            # Create ORM object
            db_review = Review(
                text=review_text,
                sentiment=result['label'],
                confidence=result['confidence']
            )
            session.add(db_review)
            count += 1
            if count % 10 == 0:
                print(f"[*] Processed {count} reviews...")
        except Exception as e:
            print(f"[!] Error processing row: {e}")

    session.commit()
    session.close()
    print(f"[\u2713] Successfully seeded {count} records into the database.")

if __name__ == "__main__":
    seed_database()

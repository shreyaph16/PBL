import os
from dotenv import load_dotenv

# Ensure environment variables are loaded if this module is imported independently
load_dotenv()

CONFIG = {
    "csv_path": "",  # Will be set dynamically
    "text_column": "review",  # Matches the column in laptops_dataset_final_600.csv
    "gemini_model": "gemini-3-flash-preview",
    "roberta_model": "cardiffnlp/twitter-roberta-base-sentiment"
}

# API KEY SETUP
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "Insert API Key Here")

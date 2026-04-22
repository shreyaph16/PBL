from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os
import tempfile
from backend.models.schemas import ProductResponse
from ml_pipeline.sentiment_engine import run_analysis

router = APIRouter(prefix="/products", tags=["Products"])

CSV_PATH = "laptops_dataset_final_600.csv"

@router.get("", response_model=ProductResponse)
def get_products():
    if not os.path.exists(CSV_PATH):
        return {"products": []}
    
    try:
        df = pd.read_csv(CSV_PATH, usecols=["product_name"])
        unique_products = df["product_name"].dropna().unique().tolist()
        unique_products.sort()
        return {"products": unique_products}
    except Exception as e:
        print(f"Error reading products: {e}")
        return {"products": []}

# Using :path to allow products with slashes (common in specs like 8GB/256GB)
@router.get("/reviews/{product_name:path}")
def get_product_reviews(product_name: str):
    if not os.path.exists(CSV_PATH):
        return {"reviews": []}
    
    try:
        df = pd.read_csv(CSV_PATH)
        mask = df["product_name"] == product_name
        if not mask.any():
            clean_name = product_name.strip(".")
            mask = df["product_name"].str.contains(clean_name, case=False, na=False)
        
        product_reviews = df[mask]["review"].dropna().tolist()
        return {"reviews": product_reviews[:15]}
    except Exception as e:
        print(f"Error fetching reviews for {product_name}: {e}")
        return {"reviews": []}

@router.post("/analyze-all/{product_name:path}")
def analyze_all_product_reviews(product_name: str):
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Primary dataset not found")

    try:
        df = pd.read_csv(CSV_PATH)
        mask = df["product_name"] == product_name
        if not mask.any():
            # Fallback for slightly different names
            clean_name = product_name.strip(".")
            mask = df["product_name"].str.contains(clean_name, case=False, na=False)
        
        subset = df[mask].copy()
        if subset.empty:
            raise HTTPException(status_code=404, detail="Product not found in dataset")
        
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            subset.to_csv(tmp.name, index=False)
            temp_path = tmp.name
        
        result = run_analysis(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return result
    except Exception as e:
        print(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

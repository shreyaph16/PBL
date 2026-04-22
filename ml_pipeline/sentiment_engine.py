import json
from ml_pipeline.graph_builder import create_sentiment_graph
from ml_pipeline.roberta_handler import roberta_handler
from ml_pipeline.config import CONFIG

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes a single piece of text for sentiment.
    Used by the FastAPI reviews endpoint.
    """
    roberta_handler.load_model()
    scores = roberta_handler.polarity_scores(text)
    
    # Map back to label/confidence for backend consistency
    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    scores_array = [scores['roberta_neg'], scores['roberta_neu'], scores['roberta_pos']]
    import numpy as np
    label_idx = np.argmax(scores_array)
    
    return {
        "label": label_map[label_idx],
        "confidence": float(scores_array[label_idx])
    }

def run_analysis(target_file_path: str) -> dict:
    """
    Main entry point for batch analysis from a CSV file.
    """
    print(f"\n[SENTIMENT ENGINE] Starting batch analysis on {target_file_path}")
    
    graph = create_sentiment_graph()
    
    initial_state = {
        "csv_data": [],
        "sentiment_score": "",
        "reasoning_summary": "",
        "input_file_path": target_file_path,
        "model_predictions": [],
        "row_count": 0,
        "sentiment_distribution": {},
        "final_sentiment_score": None,
        "average_sentiment_scores": None,
        "final_detailed_predictions": None,
        "final_metadata": None
    }

    try:
        result_state = graph.invoke(initial_state)
        
        return {
            "status": "success",
            "file_analyzed": target_file_path,
            "overall_sentiment": result_state['final_sentiment_score'],
            "reasoning_summary": result_state['reasoning_summary'],
            "sentiment_distribution": result_state['sentiment_distribution'],
            "average_scores": result_state['average_sentiment_scores'],
            "metadata": result_state['final_metadata'],
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "file_analyzed": target_file_path
        }

if __name__ == "__main__":
    # Quick CLI test
    import os
    import pandas as pd
    test_file = "test_data.csv"
    if not os.path.exists(test_file):
        df = pd.DataFrame({"review": ["I love this!", "Absolute rubbish.", "Not bad."] })
        df.to_csv(test_file, index=False)
    
    result = run_analysis(test_file)
    print(json.dumps(result, indent=2))
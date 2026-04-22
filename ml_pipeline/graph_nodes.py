import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from ml_pipeline.state import GraphState
from ml_pipeline.config import CONFIG, GEMINI_API_KEY
from ml_pipeline.roberta_handler import roberta_handler

def load_csv_data(state: GraphState) -> GraphState:
    """Node A: Load CSV data from file."""
    print(">>> NODE: LOAD CSV DATA")
    csv_path = state["input_file_path"]

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    df = None
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            break
        except Exception:
            continue

    if df is None:
        raise ValueError(f"Could not read CSV with any standard encoding")

    # Verify required columns exist
    text_col = CONFIG["text_column"]
    if text_col not in df.columns:
        # Fallback check
        found = False
        for col in df.columns:
            if col.lower() == text_col.lower():
                df.rename(columns={col: text_col}, inplace=True)
                found = True
                break
        if not found:
            # Fallback to 'review' or 'content' or first object column
            for col in ['review', 'content', 'text']:
                if col in df.columns:
                    df.rename(columns={col: text_col}, inplace=True)
                    found = True
                    break
        if not found:
            raise ValueError(f"Required text column not found. Checked: {text_col}")

    df[text_col] = df[text_col].fillna("")
    csv_data = df.to_dict('records')
    return {**state, "csv_data": csv_data, "row_count": len(csv_data)}

def classifier_agent(state: GraphState) -> GraphState:
    """Node B: Run RoBERTa."""
    print(">>> NODE: SENTIMENT CLASSIFICATION")
    csv_data = state["csv_data"]
    texts = [str(row.get(CONFIG["text_column"], "")) for row in csv_data]

    # Limit to 50 for performance in this flow if needed, but for now we follow the engine
    predictions = roberta_handler.predict_batch(texts[:100]) # Sample for speed

    predicted_labels = []
    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}

    for pred in predictions:
        scores_array = [pred['roberta_neg'], pred['roberta_neu'], pred['roberta_pos']]
        label_idx = np.argmax(scores_array)
        predicted_labels.append(label_map[label_idx])

    sentiment_counts = pd.Series(predicted_labels).value_counts().to_dict()
    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else "Neutral"

    for i, pred in enumerate(predictions):
        pred['predicted_label'] = predicted_labels[i]

    return {
        **state,
        "sentiment_score": overall_sentiment,
        "model_predictions": predictions,
        "sentiment_distribution": sentiment_counts
    }

def reasoning_agent(state: GraphState) -> GraphState:
    """Node C: Generate detailed summary using Gemini API."""
    print(">>> NODE: LLM REASONING")

    if not GEMINI_API_KEY or GEMINI_API_KEY == "Insert API Key Here":
        print("[LLM] Skipping Gemini reasoning (No valid API Key).")
        return {**state, "reasoning_summary": "Gemini reasoning skipped. Please provide an API key."}

    try:
        llm = ChatGoogleGenerativeAI(
            model=CONFIG["gemini_model"],
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )

        # Prepare summary data
        sentiment_score = state["sentiment_score"]
        predictions = state["model_predictions"]
        sentiment_dist = state["sentiment_distribution"]
        csv_data = state["csv_data"]

        data_summary = []
        valid_rows = [(row, pred) for row, pred in zip(csv_data, predictions) if row.get(CONFIG["text_column"])]

        for i, (row, pred) in enumerate(valid_rows[:10]):
            text = str(row.get(CONFIG["text_column"], ""))
            text_preview = text[:100] + "..." if len(text) > 100 else text
            label = pred['predicted_label']
            confidence = max(pred['roberta_neg'], pred['roberta_neu'], pred['roberta_pos'])
            data_summary.append(f'{i + 1}. [{label.upper()} - {confidence:.2%}] "{text_preview}"')

        data_summary_text = "\n".join(data_summary)

        # Calculate averages safely
        avg_neg = np.mean([p['roberta_neg'] for p in predictions]) if predictions else 0
        avg_neu = np.mean([p['roberta_neu'] for p in predictions]) if predictions else 0
        avg_pos = np.mean([p['roberta_pos'] for p in predictions]) if predictions else 0

        prompt = f"""As an expert sentiment analyst, provide a **concise, 2-3 sentence summary** for stakeholders. 
        Explain what the majority of reviews say about the product based on these metrics:

        OVERALL SENTIMENT: {sentiment_score}
        DISTRIBUTION: {json.dumps(sentiment_dist)}
        AVG SCORES: Neg {avg_neg:.2f}, Neu {avg_neu:.2f}, Pos {avg_pos:.2f}

        SAMPLE REVIEWS:
        {data_summary_text}
        """

        response = llm.invoke(prompt)
        return {**state, "reasoning_summary": response.content}
    except Exception as e:
        print(f"[LLM] Error: {e}")
        return {**state, "reasoning_summary": "Error generating summary with Gemini."}

def format_output(state: GraphState) -> GraphState:
    """Node D: Structure final result."""
    predictions = state["model_predictions"]

    if predictions:
        avg_scores = {
            "average_negative": float(np.mean([p['roberta_neg'] for p in predictions])),
            "average_neutral": float(np.mean([p['roberta_neu'] for p in predictions])),
            "average_positive": float(np.mean([p['roberta_pos'] for p in predictions]))
        }
    else:
        avg_scores = {"average_negative": 0.0, "average_neutral": 0.0, "average_positive": 0.0}

    metadata = {
        "total_rows": state["row_count"],
        "model_used": CONFIG["roberta_model"],
        "timestamp": datetime.now().isoformat()
    }

    return {
        **state,
        "final_sentiment_score": state["sentiment_score"],
        "average_sentiment_scores": avg_scores,
        "final_detailed_predictions": state["model_predictions"][:50],
        "final_metadata": metadata
    }

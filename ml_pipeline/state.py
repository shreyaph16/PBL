from typing import TypedDict, List, Dict, Optional

class GraphState(TypedDict):
    """TypedDict for carrying information between graph nodes."""
    csv_data: List[Dict]
    sentiment_score: str
    reasoning_summary: str
    input_file_path: str
    model_predictions: List[Dict]
    row_count: int
    sentiment_distribution: Dict
    final_sentiment_score: Optional[str]
    average_sentiment_scores: Optional[Dict[str, float]]
    final_detailed_predictions: Optional[List[Dict]]
    final_metadata: Optional[Dict]

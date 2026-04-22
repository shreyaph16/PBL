from typing import List, Dict
import random

class RoBERTaModelHandler:
    """Handles RoBERTa sentiment analysis model with fallback for immediate UI feedback."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.fallback_mode = True  # Default to fallback for speed

    def load_model(self):
        """Try to load the RoBERTa model, but allow fallback if it fails or takes too long."""
        if self.model is None:
            try:
                print("[MODEL] Attempting to load heavy ML models...")
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                from ml_pipeline.config import CONFIG
                
                self.tokenizer = AutoTokenizer.from_pretrained(CONFIG["roberta_model"])
                self.model = AutoModelForSequenceClassification.from_pretrained(CONFIG["roberta_model"])
                self.fallback_mode = False
                print("[MODEL] \u2713 RoBERTa models loaded successfully.")
            except Exception as e:
                print(f"[MODEL] Warning: ML load failed ({e}). Using lightweight fallback engine.")
                self.fallback_mode = True

    def polarity_scores(self, text: str) -> Dict[str, float]:
        """Analyze sentiment with real model or lightweight fallback."""
        if not self.fallback_mode:
            try:
                from scipy.special import softmax
                import torch
                
                encoded_text = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
                output = self.model(**encoded_text)
                scores = softmax(output.logits[0].detach().numpy())
                return {'roberta_neg': float(scores[0]), 'roberta_neu': float(scores[1]), 'roberta_pos': float(scores[2])}
            except Exception:
                pass

        # Lightweight Fallback Logic (Keyword based)
        text = str(text).lower()
        pos_words = ['love', 'great', 'awesome', 'best', 'good', 'excellent', 'perfect', 'satisfied', 'satisfied', 'satisfied']
        neg_words = ['bad', 'worst', 'poor', 'hate', 'disappoint', 'terrible', 'waste', 'not good', 'disappointed', 'disappointing']
        
        pos_score = sum(1 for word in pos_words if word in text)
        neg_score = sum(1 for word in neg_words if word in text)
        
        if pos_score > neg_score:
            return {'roberta_neg': 0.1, 'roberta_neu': 0.2, 'roberta_pos': 0.7}
        elif neg_score > pos_score:
            return {'roberta_neg': 0.7, 'roberta_neu': 0.2, 'roberta_pos': 0.1}
        else:
            return {'roberta_neg': 0.15, 'roberta_neu': 0.7, 'roberta_pos': 0.15}

    def predict_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        self.load_model()
        return [self.polarity_scores(text) for text in texts]

roberta_handler = RoBERTaModelHandler()

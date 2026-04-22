import logging
import traceback
from backend.models.schemas import AnalyzeResponse
from backend.core.exceptions import MLServiceError
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings

logger = logging.getLogger(__name__)

# ── Import from the untouched ML pipeline ─────────────────────────────────────
from ml_pipeline.sentiment_engine import analyze_sentiment


def run_sentiment_analysis(text: str) -> AnalyzeResponse:
    """
    Bridge between FastAPI and the ML pipeline.
    """
    if not text or not text.strip():
        raise MLServiceError("Input text must not be empty.")

    try:
        raw: dict = analyze_sentiment(text.strip())
    except Exception as exc:
        logger.error("ML pipeline raised an exception: %s", exc, exc_info=True)
        raise MLServiceError(f"Pipeline error: {exc}") from exc

    # Validate contract
    if not isinstance(raw, dict) or "label" not in raw or "confidence" not in raw:
        logger.error("Unexpected ML pipeline response: %s", raw)
        raise MLServiceError("ML pipeline returned an unexpected response format.")

    label = str(raw["label"]).lower()
    if label not in {"positive", "negative", "neutral"}:
        logger.warning("Unrecognised label '%s' — defaulting to 'neutral'", label)
        label = "neutral"

    confidence = float(raw["confidence"])
    confidence = max(0.0, min(1.0, confidence))   # clamp to [0, 1]

    # ── Generate Reasoning with Gemini if available ──────────────────────────────
    reasoning = None
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "Insert API Key Here":
        try:
            # Use configurable model from settings
            llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, google_api_key=settings.GEMINI_API_KEY)
            prompt = f"Explain in one sentence why this review is {label}: \"{text}\""
            response = llm.invoke(prompt)
            reasoning = response.content
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                reasoning = f"Gemini Quota Exceeded for {settings.GEMINI_MODEL}. Please wait or switch models."
            elif "404" in error_msg:
                reasoning = f"Gemini Model {settings.GEMINI_MODEL} not found. Check your configuration."
            else:
                reasoning = f"AI reasoning unavailable (Model error). Detection suggests {label} sentiment."
            
            logger.warning("Gemini reasoning failed for %s: %s", settings.GEMINI_MODEL, e)
            logger.debug(traceback.format_exc())
    else:
        reasoning = "Gemini API key not configured. Enable it in .env to see detailed reasoning."

    return AnalyzeResponse(label=label, confidence=confidence, reasoning=reasoning)
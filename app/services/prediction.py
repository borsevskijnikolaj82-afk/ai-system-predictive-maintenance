from uuid import uuid4
from app.ml.preprocessing import transform
from app.ml.inference import ModelLoader


class PredictionService:
    def __init__(self, model: ModelLoader, review_threshold: float = 0.8) -> None:
        self.model = model
        self.review_threshold = review_threshold

    def predict(self, payload: dict) -> dict:
        result = self.model.predict(transform(payload))
        return {
            "request_id": str(uuid4()),
            "item_id": payload["item_id"],
            "prediction": result.prediction,
            "probability": result.probability,
            "model_version": self.model.version,
            "manual_review_required": result.probability < self.review_threshold,
        }

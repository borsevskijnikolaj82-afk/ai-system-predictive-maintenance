from dataclasses import dataclass
import numpy as np


@dataclass
class InferenceResult:
    prediction: str
    probability: float


class ModelLoader:
    """Educational stub: real weights are kept outside Git."""

    def __init__(self, version: str = "1.0.0") -> None:
        self.version = version
        self.loaded = True

    def predict(self, features: np.ndarray) -> InferenceResult:
        temperature, vibration, operating_hours, error_code = features.tolist()
        risk_score = min(
            1.0,
            max(0.0, 0.003 * max(temperature - 70, 0) + 0.05 * vibration + 0.00005 * operating_hours + 0.01 * error_code),
        )
        if risk_score >= 0.75:
            label = "CRITICAL_RISK"
        elif risk_score >= 0.45:
            label = "WARNING_ANOMALY"
        else:
            label = "NORMAL"
        return InferenceResult(label, round(risk_score, 4))

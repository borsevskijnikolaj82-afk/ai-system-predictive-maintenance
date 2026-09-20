import numpy as np


def transform(payload: dict) -> np.ndarray:
    """Versioned feature transformation used by the serving path."""
    return np.asarray(
        [
            payload["temperature"],
            payload["vibration_amplitude"],
            payload["operating_hours"],
            payload["error_code_last_24h"],
        ],
        dtype=float,
    )

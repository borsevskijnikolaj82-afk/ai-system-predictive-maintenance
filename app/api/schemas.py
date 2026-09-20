from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1, max_length=128)
    temperature: float = Field(ge=-50.0, le=250.0, description="Температура узла, °C")
    vibration_amplitude: float = Field(ge=0.0, le=100.0, description="Амплитуда вибрации, мм/с")
    operating_hours: int = Field(ge=0, description="Наработка в часах")
    error_code_last_24h: int = Field(default=0, ge=0, le=999)


class PredictionResponse(BaseModel):
    request_id: str
    item_id: str
    prediction: str
    probability: float = Field(ge=0.0, le=1.0)
    model_version: str
    manual_review_required: bool


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str
    uptime_seconds: int

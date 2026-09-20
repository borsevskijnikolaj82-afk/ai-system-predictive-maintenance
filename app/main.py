from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import configure_logging
from app.ml.inference import ModelLoader
from app.repositories.in_memory import PredictionRepository
from app.services.prediction import PredictionService

configure_logging()
app = FastAPI(title="Predictive Maintenance AI Service", version="1.0.0")
model = ModelLoader("1.0.0")
prediction_service = PredictionService(model)
repository = PredictionRepository()
app.include_router(router)

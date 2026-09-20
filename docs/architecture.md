# Architecture Blueprint

## Контуры
1. DataOps: источники телеметрии, валидация схем и версионирование данных.
2. MLOps: обучение, валидация, реестр моделей и хранение весов.
3. Application & Serving: FastAPI, API-key, validation, preprocessing, inference, business logic.
4. DevOps & Observability: Docker, CI/CD, JSON logs, Prometheus, Evidently.

## Data Flow
Клиент → HTTPS/JSON → API Gateway → Pydantic → preprocessing → inference → business rules → repository → JSON response.

## Train-Serving Skew
Предобработка должна быть единым версионируемым артефактом для train и serving.

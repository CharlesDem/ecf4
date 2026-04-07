from fastapi import FastAPI
import uvicorn
import joblib
from tensorflow import keras as tf_keras

from router import api_router
from exception_handlers import register_exception_handlers
from logging_utils import register_request_logging, setup_logger
from swagger_content import API_DESCRIPTION, API_TITLE, API_VERSION, OPENAPI_TAGS, build_openapi

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url=None,
    openapi_tags=OPENAPI_TAGS,
)
app.include_router(api_router)
app.openapi = build_openapi(app)


logger = setup_logger()
register_request_logging(app, logger)
register_exception_handlers(app, logger)


def load_artifacts() -> None:
    model_path = "../models/best_model.keras"
    vectorizer_path = "../models/vectorizer.pkl"
    app.state.model = tf_keras.models.load_model(model_path, compile=False)
    app.state.vectorizer = joblib.load(vectorizer_path)
    logger.info("artifacts loaded | model=%s | vectorizer=%s", model_path, vectorizer_path)


load_artifacts()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

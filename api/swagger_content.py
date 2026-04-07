from copy import deepcopy

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

API_TITLE = "Fake News Detector API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API de classification de titres en fake/real (fort biais élections américaines 2016)."
OPENAPI_TAGS = [
    {"name": "health", "description": "etat de l'api"},
    {"name": "fake_news_detector", "description": "prediction sur un titre ou un batch"},
]

SCHEMA_EXAMPLES = {
    "TitleInput": {"title": "Hillary is finally a reptilian, Utah farmer said"},
    "TitlesInput": {
        "titles": [
            "parliament votes on new environmental legislation",
            "you will not believe what this celebrity did last night",
        ]
    },
    "PredictionResponse": {
        "title": "parliament votes on new environmental legislation",
        "label": "REAL",
        "confidence": 0.91,
    },
    "PredictionsResponse": {
        "predictions": [
            {
                "title": "parliament votes on new environmental legislation",
                "label": "REAL",
                "confidence": 0.91,
            },
            {
                "title": "you will not believe what this celebrity did last night",
                "label": "FAKE",
                "confidence": 0.88,
            },
        ]
    },
}


def build_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=API_TITLE,
            version=API_VERSION,
            description=API_DESCRIPTION,
            routes=app.routes,
            tags=OPENAPI_TAGS,
        )
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        for schema_name, example in SCHEMA_EXAMPLES.items():
            if schema_name in components:
                components[schema_name]["example"] = deepcopy(example)

        app.openapi_schema = schema
        return app.openapi_schema

    return custom_openapi

from fastapi import Request
import numpy as np

from fake_news_detector.model import PredictionResponse, PredictionsResponse, TitleInput, TitlesInput


class FakeNewsDetectorService:

    def __init__(self, model, vectorizer) -> None:
        self.model = model
        self.vectorizer = vectorizer

    def predict(self, payload: TitleInput) -> PredictionResponse:

        predictions = self._predict_proba([payload.title])

        probability_real = float(predictions[0])
        label = "REAL" if probability_real >= 0.5 else "FAKE"
        confidence = probability_real if label == "REAL" else 1 - probability_real

        return PredictionResponse(title=payload.title, label=label, confidence=round(confidence, 4))

    def predict_batch(self, payload: TitlesInput) -> PredictionsResponse:

        predictions = self._predict_proba(payload.titles)

        items: list[PredictionResponse] = []
        for title, probability_real in zip(payload.titles, predictions):
            label = "REAL" if probability_real >= 0.5 else "FAKE"
            confidence = probability_real if label == "REAL" else 1 - probability_real
            items.append(PredictionResponse(title=title, label=label, confidence=round(float(confidence), 4)))

        return PredictionsResponse(predictions=items)

    def _predict_proba(self, titles: list[str]) -> np.ndarray:

        vectors = self.vectorizer.transform(titles)

        raw = self.model.predict(vectors.toarray(), verbose=0)

        proba = np.asarray(raw).reshape(-1)
        
        return np.clip(proba, 0.0, 1.0)


def get_fake_news_detector_service(request: Request) -> FakeNewsDetectorService:
    return FakeNewsDetectorService(
        model=request.app.state.model,
        vectorizer=request.app.state.vectorizer,
    )

from fastapi import APIRouter, Depends

from fake_news_detector.model import PredictionResponse, PredictionsResponse, TitleInput, TitlesInput
from fake_news_detector.service import FakeNewsDetectorService, get_fake_news_detector_service

router = APIRouter(tags=["fake_news_detector"])


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: TitleInput,
    service: FakeNewsDetectorService = Depends(get_fake_news_detector_service),
) -> PredictionResponse:
    """ Given a news title, the API will return REAL or FAKE news, including  confidence score"""
    return service.predict(payload)


@router.post("/predict/batch", response_model=PredictionsResponse)
def predict_batch(
    payload: TitlesInput,
    service: FakeNewsDetectorService = Depends(get_fake_news_detector_service),
) -> PredictionsResponse:
    """ Given several news title, the API will return REAL or FAKE news for each, including  confidence score"""
    return service.predict_batch(payload)

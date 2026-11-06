"""
RythuCrop Crop Recommender Engine & In-Memory Cache Wrapper
Provides thread-safe access and eager pre-warming for the Random Forest
Crop Recommendation Model and agronomic bounds dataset.
"""

import threading
from typing import Dict, Any, List, Optional

from app.models.predictor import (
    CropInputError,
    load_recommendation_model,
    get_crop_agronomic_stats,
    recommend_crop,
    recommend_crop_top3,
    recommend_crop_top3_detailed,
    recommend_farm_plan,
    recommend_farm_plan_detailed,
    FEATURE_COLUMNS,
    INPUT_RANGES,
    CROP_CHARACTERISTICS,
    FARM_PLANNING_CROPS,
    MODEL_PATH,
    BASE_DIR
)


def prewarm_crop_recommender() -> bool:
    """
    Eagerly loads ML recommendation artifacts into memory.
    Eliminates disk I/O latency on initial prediction requests.
    """
    try:
        model = load_recommendation_model()
        stats = get_crop_agronomic_stats()
        return model is not None and stats is not None
    except Exception:
        return False


# In-memory pre-warming upon module import
try:
    prewarm_crop_recommender()
except Exception:
    pass


__all__ = [
    "CropInputError",
    "load_recommendation_model",
    "get_crop_agronomic_stats",
    "recommend_crop",
    "recommend_crop_top3",
    "recommend_crop_top3_detailed",
    "recommend_farm_plan",
    "recommend_farm_plan_detailed",
    "prewarm_crop_recommender",
    "FEATURE_COLUMNS",
    "INPUT_RANGES",
    "CROP_CHARACTERISTICS",
    "FARM_PLANNING_CROPS",
    "MODEL_PATH",
    "BASE_DIR"
]

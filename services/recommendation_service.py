"""High-level recommendation service that exposes recommendation and suggestion APIs."""
import time
from typing import Dict, List, Optional
from services.preprocess import load_movies
from models.recommender import Recommender
from config import DATASET_PATH


class RecommendationService:
    """Load dataset and provide recommendation and suggestion APIs."""

    def __init__(self):
        self.df = load_movies(DATASET_PATH)
        self.recommender = Recommender(self.df)

    def get_recommendations(
        self,
        query: str,
        top_n: int = 5,
        genre: Optional[str] = None,
        language: Optional[str] = None,
        min_rating: Optional[float] = None,
        year: Optional[int] = None,
    ) -> Dict[str, object]:
        start_time = time.perf_counter()
        items = self.recommender.recommend(
            query=query,
            top_n=top_n,
            genre=genre,
            language=language,
            min_rating=min_rating,
            year=year,
        )
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            'recommendations': items,
            'debug': {
                'dataset_size': len(self.df),
                'tfidf_feature_count': self.recommender.feature_count,
                'recommendation_count': len(items),
                'processing_time_ms': elapsed_ms,
            },
        }

    def search_suggestions(self, query: str, limit: int = 8) -> List[str]:
        prefix = str(query or '').strip().lower()
        if not prefix:
            return []

        suggestions = []
        for source in [self.df['title'], self.df['genre'], self.df['language']]:
            for value in source.dropna().unique():
                normalized = str(value).strip()
                if normalized and prefix in normalized.lower():
                    suggestions.append(normalized)

        unique_suggestions = []
        for item in suggestions:
            if item not in unique_suggestions:
                unique_suggestions.append(item)
            if len(unique_suggestions) >= limit:
                break

        return unique_suggestions

    def get_filters(self) -> Dict[str, List[str]]:
        return {
            'genres': sorted({str(value).strip() for value in self.df['genre'].dropna().unique() if value}),
            'languages': sorted({str(value).strip() for value in self.df['language'].dropna().unique() if value}),
            'years': sorted({int(value) for value in self.df['year'].dropna().astype(int).unique() if value > 0}),
        }


service = RecommendationService()

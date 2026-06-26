"""Core recommender model using TF-IDF and cosine similarity."""
from typing import Any, Dict, List, Optional
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from services.tfidf_engine import TfidfEngine
from services.similarity_engine import query_similarity
from services.tmdb_client import get_poster_url


class Recommender:
    """Recommender system that builds TF-IDF on combined features."""

    def __init__(self, df: pd.DataFrame):
        self.df = self._prepare_dataframe(df)
        # ensure a poster_url column exists to allow caching fetched posters
        if 'poster_url' not in self.df.columns:
            self.df['poster_url'] = ''
        # try to load a persistent poster map (one-time pre-population)
        try:
            from config import POSTER_MAP_PATH
            if POSTER_MAP_PATH and os.path.exists(POSTER_MAP_PATH):
                poster_map = pd.read_csv(POSTER_MAP_PATH)
                if 'id' in poster_map.columns and 'poster_url' in poster_map.columns:
                    poster_map = poster_map.set_index('id')
                    def _map_poster(x):
                        try:
                            return poster_map.at[int(x), 'poster_url']
                        except Exception:
                            return ''
                    self.df['poster_url'] = self.df['id'].apply(_map_poster).fillna('').astype(str)
        except Exception:
            pass
        self.tfidf = TfidfEngine()
        self.matrix = self.tfidf.fit(self.df['combined_features'])
        self.feature_count = len(self.tfidf.vectorizer.get_feature_names_out())

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy().fillna('')
        df['genre'] = df['genre'].astype(str)
        df['language'] = df['language'].astype(str)
        df['title'] = df['title'].astype(str)
        df['description'] = df['description'].astype(str)
        df['combined_features'] = (
            df['genre'].str.lower() + ' ' +
            df['language'].str.lower() + ' ' +
            df['title'].str.lower() + ' ' +
            df['description'].str.lower()
        )
        return df.reset_index(drop=True)

    def _clean_query(self, text: str) -> str:
        return str(text or '').strip().lower()

    def _explain_item(self, row: pd.Series, query: str) -> List[str]:
        reasons: List[str] = []
        query_tokens = {token for token in query.split() if len(token) > 2}
        if any(tag in query_tokens for tag in row['genre'].lower().split()):
            reasons.append('✓ Similar Genre')
        if row['language'].strip().lower() in query:
            reasons.append('✓ Similar Language')
        if any(word in row['description'].lower() for word in query_tokens):
            reasons.append('✓ Similar Description')
        if any(part in row['title'].lower() for part in query_tokens):
            reasons.append('✓ Similar User Preference')
        return reasons or ['✓ Relevant content based on your search']

    def _format_result(self, row: pd.Series, score: float, query: str) -> Dict[str, Any]:
        match_percentage = round(score * 100, 2)
        if score > 0 and match_percentage < 1.0:
            match_percentage = 1.0
        # resolve poster (use cached value if present)
        poster = row.get('poster_url') or None
        if not poster:
            try:
                poster = get_poster_url(row.get('title', ''), row.get('year'))
            except Exception:
                poster = ''

        # attempt to cache resolved poster URL back into the dataframe
        try:
            if not row.get('poster_url') and poster:
                self.df.at[row.name, 'poster_url'] = poster
        except Exception:
            pass

        return {
            'id': int(row['id']),
            'title': row['title'],
            'genre': row['genre'],
            'language': row['language'],
            'rating': float(row['rating']),
            'year': int(row['year']),
            'description': row['description'],
            'similarity_score': round(score, 4),
            'match': match_percentage,
            'explanation': self._explain_item(row, query),
            'poster_url': poster or '/static/images/logo.png',
        }

    def recommend(
        self,
        query: str,
        top_n: int = 5,
        genre: Optional[str] = None,
        language: Optional[str] = None,
        min_rating: Optional[float] = None,
        year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        query_text = self._clean_query(query)
        if not query_text:
            return []

        query_vector = self.tfidf.transform([query_text])
        similarity_scores = query_similarity(query_vector, self.matrix)
        self.df['score'] = similarity_scores

        filtered = self.df.copy()
        if genre and genre.lower() != 'all':
            filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
        if language and language.lower() != 'all':
            filtered = filtered[filtered['language'].str.contains(language, case=False, na=False)]
        if min_rating is not None:
            filtered = filtered[filtered['rating'] >= min_rating]
        if year is not None and year > 0:
            filtered = filtered[filtered['year'] == year]

        filtered = filtered.sort_values('score', ascending=False)
        results: List[Dict[str, Any]] = []

        for _, row in filtered.iterrows():
            score = float(row['score'])
            if score <= 0:
                continue
            results.append(self._format_result(row, score, query_text))
            if len(results) >= top_n:
                break

        if not results:
            direct_matches = self.df[self.df['title'].str.contains(query_text, case=False, na=False)]
            for _, row in direct_matches.head(top_n).iterrows():
                results.append(self._format_result(row, 0.0, query_text))
            if results:
                return results

            fallback_matches = self.df[
                self.df['genre'].str.contains(query_text, case=False, na=False)
                | self.df['description'].str.contains(query_text, case=False, na=False)
            ]
            for _, row in fallback_matches.head(top_n).iterrows():
                results.append(self._format_result(row, 0.0, query_text))

        return results

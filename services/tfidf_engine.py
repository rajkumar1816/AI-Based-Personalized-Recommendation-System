"""Wrapper around TF-IDF vectorizer."""
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEngine:
    """Encapsulate TF-IDF fitting and transforming."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def fit(self, documents):
        """Fit the vectorizer to documents."""
        return self.vectorizer.fit_transform(documents)

    def transform(self, documents):
        """Transform documents with fitted vectorizer."""
        return self.vectorizer.transform(documents)

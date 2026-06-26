"""Similarity computations using cosine similarity."""
from typing import List
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity_matrix(matrix):
    """Compute item-to-item cosine similarity matrix."""
    return cosine_similarity(matrix)


def query_similarity(vector, matrix) -> List[float]:
    """Compute similarity scores between a query vector and a document matrix."""
    return cosine_similarity(vector, matrix).flatten()

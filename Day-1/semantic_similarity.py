"""
Day 1 - Exercise 2: Semantic Similarity Calculator
"""

import math
from typing import List


class SemanticSimilarity:
    """Calculate cosine similarity between numeric vectors."""

    def __init__(self):
        print("Semantic Similarity Calculator ready")

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Return cosine similarity between vec1 and vec2.

        Returns 0.0 for zero-length vectors.
        """
        if len(vec1) != len(vec2):
            raise ValueError(f"Vectors must be same length! Got {len(vec1)} and {len(vec2)}")

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    def interpret_similarity(self, score: float) -> str:
        """Map numeric similarity to a human-friendly label."""
        if score >= 0.9:
            return "Nearly identical!"
        elif score >= 0.7:
            return "Very similar"
        elif score >= 0.5:
            return "Somewhat similar"
        elif score >= 0.3:
            return "A bit related"
        else:
            return "Quite different"

    def compare_multiple(self, base_vec: List[float], compare_vecs: dict) -> dict:
        """Compare base_vec to many vectors and return sorted results."""
        results = {}
        for name, vec in compare_vecs.items():
            similarity = self.cosine_similarity(base_vec, vec)
            results[name] = similarity

        sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
        return sorted_results


if __name__ == "__main__":
    sim = SemanticSimilarity()
    vec_king = [0.8, 0.6]
    vec_queen = [0.7, 0.5]
    vec_car = [0.2, 0.9]
    vec_truck = [0.3, 0.8]
    vec_dog = [0.6, 0.3]
    vec_cat = [0.5, 0.2]

    print(f"King <-> Queen: {sim.cosine_similarity(vec_king, vec_queen):.3f}")
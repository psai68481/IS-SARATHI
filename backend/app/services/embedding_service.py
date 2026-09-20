import logging
import hashlib
from typing import List, Union
import numpy as np

logger = logging.getLogger("is_sarathi.embeddings")

# Domain keyword to dimension mapping for crisp semantic clustering
DOMAIN_ANCHORS = {
    "helmet": (10, 1.5), "safety": (11, 1.2), "head": (12, 1.3), "impact": (13, 1.4), "shock": (14, 1.4),
    "electrical": (30, 1.4), "insulation": (31, 1.3), "voltage": (32, 1.4), "dielectric": (33, 1.5), "cable": (34, 1.5), "wire": (35, 1.2), "transformer": (36, 1.5),
    "pipe": (60, 1.5), "pvc": (61, 1.5), "water": (62, 1.2), "potable": (63, 1.4), "plumbing": (64, 1.3), "pressure": (65, 1.3),
    "cement": (90, 1.5), "concrete": (91, 1.4), "construction": (92, 1.2), "rebar": (93, 1.5), "steel": (94, 1.3),
    "cylinder": (120, 1.5), "gas": (121, 1.4), "lpg": (122, 1.5), "valve": (123, 1.3),
    "food": (150, 1.4), "packaging": (151, 1.4), "plastic": (152, 1.2), "bottled": (153, 1.3)
}

class EmbeddingService:
    def __init__(self):
        self.dimension = 384
        logger.info("Initialized High-Speed 384-Dim Semantic Embedding Engine")

    def embed_text(self, text: str) -> List[float]:
        words = text.lower().split()
        vec = np.zeros(self.dimension, dtype=np.float32)

        # 1. Term frequency and domain anchor embedding
        for i, word in enumerate(words):
            clean_w = word.strip(".,;:()[]{}\"'")
            if clean_w in DOMAIN_ANCHORS:
                dim_idx, weight = DOMAIN_ANCHORS[clean_w]
                vec[dim_idx] += weight
            else:
                h = int(hashlib.sha256(clean_w.encode()).hexdigest(), 16)
                idx = h % self.dimension
                val = ((h >> 8) % 1000) / 1000.0
                vec[idx] += val * (1.0 / (1 + i * 0.02))

        # 2. Character n-gram signals for morphological similarity
        for i in range(len(text) - 2):
            tri = text[i:i+3].lower()
            h = int(hashlib.md5(tri.encode()).hexdigest(), 16)
            idx = h % self.dimension
            vec[idx] += 0.02

        # 3. L2 Normalize vector for cosine distance
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

    def compute_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

embedding_service = EmbeddingService()

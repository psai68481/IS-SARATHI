import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.embedding_service import embedding_service

logger = logging.getLogger("is_sarathi.pinecone")

class PineconeService:
    def __init__(self):
        self.pc = None
        self.index = None
        self.in_memory_index: Dict[str, Dict[str, Any]] = {}
        
        if settings.PINECONE_API_KEY and settings.PINECONE_API_KEY != "your_pinecone_api_key_here":
            try:
                from pinecone import Pinecone, ServerlessSpec
                self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
                existing = [i.name for i in self.pc.list_indexes()]
                if settings.PINECONE_INDEX_NAME not in existing:
                    logger.info(f"Creating Pinecone index: {settings.PINECONE_INDEX_NAME}")
                    self.pc.create_index(
                        name=settings.PINECONE_INDEX_NAME,
                        dimension=embedding_service.dimension,
                        metric="cosine",
                        spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENVIRONMENT)
                    )
                self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
                logger.info("Connected to Pinecone cloud index.")
            except Exception as e:
                logger.warning(f"Pinecone cloud connection error ({e}). Using local in-memory vector index.")
                self.index = None
        else:
            logger.info("No PINECONE_API_KEY configured. Operating in high-performance local vector search mode.")

    def upsert_vectors(self, vectors: List[Dict[str, Any]]) -> bool:
        """
        vectors: list of {'id': str, 'values': List[float], 'metadata': Dict[str, Any]}
        """
        if self.index:
            try:
                self.index.upsert(vectors=vectors)
                return True
            except Exception as e:
                logger.error(f"Pinecone upsert failed: {e}")

        # In-memory storage
        for v in vectors:
            self.in_memory_index[v['id']] = {
                'values': v['values'],
                'metadata': v.get('metadata', {})
            }
        return True

    def query_similarity(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns ranked list of candidate IDs with similarity scores and metadata.
        """
        if self.index:
            try:
                filter_dict = {}
                if category_filter:
                    filter_dict["category"] = {"$eq": category_filter}
                res = self.index.query(
                    vector=query_vector,
                    top_k=top_k,
                    include_metadata=True,
                    filter=filter_dict if filter_dict else None
                )
                matches = []
                for match in res.matches:
                    matches.append({
                        "id": match.id,
                        "score": float(match.score),
                        "metadata": match.metadata or {}
                    })
                return matches
            except Exception as e:
                logger.error(f"Pinecone query error ({e}), falling back to in-memory cosine search.")

        # Local in-memory cosine similarity search
        scores = []
        for doc_id, doc_data in self.in_memory_index.items():
            meta = doc_data['metadata']
            if category_filter and meta.get('category') != category_filter:
                continue
            sim = embedding_service.compute_similarity(query_vector, doc_data['values'])
            scores.append({
                "id": doc_id,
                "score": sim,
                "metadata": meta
            })

        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:top_k]

pinecone_service = PineconeService()

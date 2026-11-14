"""Sentence-Transformers real embedding provider."""
from typing import Protocol
from sentence_transformers import SentenceTransformer


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """SentenceTransformer embedding provider adapter (paraphrase-multilingual-MiniLM-L12-v2)."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        # Determine dimensions dynamically from test embedding
        test_emb = self.model.encode("test", convert_to_numpy=True)
        self.dimensions = int(len(test_emb))

    def embed_documents(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.tolist()

    def embed_query(self, question: str) -> list[float]:
        embedding = self.model.encode(
            question,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding.tolist()

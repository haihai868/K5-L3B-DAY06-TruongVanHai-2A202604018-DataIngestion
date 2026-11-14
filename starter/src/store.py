"""Persistent Vector Store using ChromaDB with cosine distance and metadata filtering."""
from typing import Any
import os
import chromadb
from .models import Chunk


class ChromaVectorStore:
    def __init__(self, persist_dir: str = "starter/data/chroma_db", dimensions: int = 384) -> None:
        self.persist_dir = persist_dir
        self.dimensions = dimensions
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)

    def get_or_create_collection(self, strategy: str):
        collection_name = f"collection_{strategy.lower()}"
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def create_schema(self) -> None:
        """Initialize collections for strategies A, B, and C."""
        for strat in ["A", "B", "C"]:
            self.get_or_create_collection(strat)

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Upsert stable chunk vectors and metadata without duplicates."""
        if not chunks:
            return
        if len(chunks) != len(vectors):
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(vectors)} vectors")

        collection = self.get_or_create_collection(strategy)
        
        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = []
        for c in chunks:
            meta = {
                "document_id": str(c.document_id),
                "source": str(c.source),
                "page": int(c.page),
                "chapter": str(c.metadata.get("chapter", "")),
                "category": str(c.metadata.get("category", "")),
                "chunk_len": int(c.metadata.get("chunk_len", len(c.text)))
            }
            metadatas.append(meta)

        # Upsert into Chroma (overwrites if ID exists)
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end = i + batch_size
            collection.upsert(
                ids=ids[i:end],
                embeddings=vectors[i:end],
                documents=documents[i:end],
                metadatas=metadatas[i:end]
            )

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Filter metadata and rank by cosine similarity, returning top-k chunks."""
        collection = self.get_or_create_collection(strategy)
        
        where_clause = None
        if filters:
            # Clean filters to simple key-value matching
            where_items = {k: v for k, v in filters.items() if v is not None}
            if len(where_items) == 1:
                where_clause = where_items
            elif len(where_items) > 1:
                where_clause = {"$and": [{k: v} for k, v in where_items.items()]}

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )

        hits: list[dict[str, Any]] = []
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                chunk_id = results["ids"][0][i]
                doc_text = results["documents"][0][i] if results["documents"] else ""
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                dist = results["distances"][0][i] if results["distances"] else 1.0
                # Cosine similarity = 1 - cosine distance
                score = round(1.0 - dist, 4)
                hits.append({
                    "chunk_id": chunk_id,
                    "text": doc_text,
                    "score": score,
                    "distance": round(dist, 4),
                    "metadata": meta
                })
                
        return hits


# Alias for backward compatibility if needed
PgVectorStore = ChromaVectorStore

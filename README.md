# Local RAG Skeleton

This project is a local prototype of a Retrieval-Augmented Generation (RAG) system.

## Goals

- Ingest local documents
- Store document & chunk metadata in PostgreSQL
- Store embeddings in a FAISS index
- Expose a simple FastAPI endpoint:
  - Input: user question
  - Output: answer + sources

## Structure

- `app/api` – FastAPI routes
- `app/core` – configuration & common utilities
- `app/rag` – embeddings, vector store, retrieval, generation
- `app/ingestion` – loaders, chunking, ingestion pipeline
- `data/raw` – input documents (local)
- `data/index` – FAISS index files
- `docs` – architecture & notes
- `tests` – basic tests

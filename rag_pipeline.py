"""
RAG Pipeline for Telecom Training Assistant
Primary: ChromaDB + HuggingFace Embeddings (requires langchain-community, chromadb)
Fallback: Pure-Python TF-IDF-like keyword retrieval (no external dependencies)
"""

import os
import re
import math
import logging
from typing import List, Tuple
from collections import defaultdict

from knowledge_base import get_all_documents
from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RETRIEVAL, CHROMA_PERSIST_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Lightweight document chunk dataclass ──────────────────────────────────────

class DocChunk:
    """Simple document chunk for retrieval."""
    def __init__(self, text: str, title: str):
        self.page_content = text
        self.metadata = {"title": title, "source": "telecom_knowledge_base"}


# ── Fallback: Pure-Python keyword retrieval ────────────────────────────────────

class KeywordRetriever:
    """
    Pure-Python TF-IDF-like retrieval.
    No external dependencies required.
    """

    def __init__(self):
        self.chunks: List[DocChunk] = []
        self.idf: dict = {}
        self._initialized = False

    def _tokenize(self, text: str) -> List[str]:
        """Lowercase, remove punctuation, split into tokens."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return [t for t in text.split() if len(t) > 2]

    def _chunk_text(self, text: str, title: str) -> List[DocChunk]:
        """Simple overlap-aware text chunker."""
        words = text.split()
        chunks = []
        step = CHUNK_SIZE - CHUNK_OVERLAP
        for i in range(0, len(words), step):
            chunk_words = words[i : i + CHUNK_SIZE]
            if chunk_words:
                chunks.append(DocChunk(" ".join(chunk_words), title))
        return chunks

    def initialize(self):
        if self._initialized:
            return
        logger.info("Building keyword retrieval index from knowledge base...")
        raw_docs = get_all_documents()

        for title, content in raw_docs:
            self.chunks.extend(self._chunk_text(content, title))

        # Compute IDF
        df: dict = defaultdict(int)
        N = len(self.chunks)
        for chunk in self.chunks:
            unique_tokens = set(self._tokenize(chunk.page_content))
            for token in unique_tokens:
                df[token] += 1
        self.idf = {t: math.log(N / (1 + freq)) for t, freq in df.items()}
        self._initialized = True
        logger.info(f"Keyword index built: {len(self.chunks)} chunks from {len(raw_docs)} documents.")

    def _score(self, query_tokens: List[str], chunk: DocChunk) -> float:
        """TF-IDF score for a chunk against query tokens."""
        chunk_tokens = self._tokenize(chunk.page_content)
        tf_counter: dict = defaultdict(int)
        for t in chunk_tokens:
            tf_counter[t] += 1
        n = len(chunk_tokens) or 1
        score = 0.0
        for qt in query_tokens:
            tf = tf_counter.get(qt, 0) / n
            idf = self.idf.get(qt, 0)
            score += tf * idf
        return score

    def retrieve(self, query: str) -> Tuple[List[DocChunk], str]:
        if not self._initialized:
            self.initialize()
        query_tokens = self._tokenize(query)
        scored = [(self._score(query_tokens, c), c) for c in self.chunks]
        scored.sort(key=lambda x: x[0], reverse=True)
        top_docs = [c for _, c in scored[:TOP_K_RETRIEVAL]]

        # Format context
        context_parts = []
        seen_titles = set()
        for doc in top_docs:
            title = doc.metadata.get("title", "Unknown")
            if title not in seen_titles:
                context_parts.append(f"### {title}\n{doc.page_content}")
                seen_titles.add(title)
            else:
                context_parts.append(doc.page_content)

        context = "\n\n---\n\n".join(context_parts)
        return top_docs, context


# ── Primary: ChromaDB + HuggingFace (optional, richer semantic retrieval) ─────

class ChromaRetriever:
    """
    Semantic retrieval using ChromaDB + sentence-transformers embeddings.
    Requires: chromadb, sentence-transformers, langchain-community
    """

    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.schema import Document

        logger.info("Loading HuggingFace embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        if os.path.exists(CHROMA_PERSIST_DIR) and os.listdir(CHROMA_PERSIST_DIR):
            logger.info("Loading persisted ChromaDB vector store...")
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=embeddings,
                collection_name="telecom_knowledge",
            )
        else:
            logger.info("Building ChromaDB vector store...")
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            all_chunks = []
            for title, content in get_all_documents():
                chunks = splitter.create_documents(
                    texts=[content],
                    metadatas=[{"title": title, "source": "telecom_knowledge_base"}],
                )
                all_chunks.extend(chunks)

            self.vectorstore = Chroma.from_documents(
                documents=all_chunks,
                embedding=embeddings,
                persist_directory=CHROMA_PERSIST_DIR,
                collection_name="telecom_knowledge",
            )
            self.vectorstore.persist()
            logger.info(f"ChromaDB built with {len(all_chunks)} chunks.")

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": TOP_K_RETRIEVAL},
        )
        self._initialized = True

    def retrieve(self, query: str):
        if not self._initialized:
            self.initialize()
        docs = self.retriever.invoke(query)
        context_parts = []
        seen_titles = set()
        for doc in docs:
            title = doc.metadata.get("title", "Unknown")
            if title not in seen_titles:
                context_parts.append(f"### {title}\n{doc.page_content}")
                seen_titles.add(title)
            else:
                context_parts.append(doc.page_content)
        context = "\n\n---\n\n".join(context_parts)
        return docs, context


# ── Auto-detect best available retriever ──────────────────────────────────────

class TelecomRAGPipeline:
    """
    Wraps either ChromaRetriever (semantic, preferred) or KeywordRetriever (fallback).
    Falls back gracefully if chromadb / langchain are not installed.
    """

    def __init__(self):
        self._backend = None
        self._mode = "uninitialized"
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        try:
            import chromadb  # noqa
            import langchain  # noqa
            import sentence_transformers  # noqa
            self._backend = ChromaRetriever()
            self._backend.initialize()
            self._mode = "semantic (ChromaDB)"
        except ImportError:
            logger.warning(
                "chromadb/langchain/sentence-transformers not available. "
                "Using pure-Python keyword retrieval fallback."
            )
            self._backend = KeywordRetriever()
            self._backend.initialize()
            self._mode = "keyword (pure-Python fallback)"
        self._initialized = True
        logger.info(f"RAG pipeline ready — mode: {self._mode}")

    def retrieve(self, query: str):
        if not self._initialized:
            self.initialize()
        return self._backend.retrieve(query)

    @property
    def mode(self) -> str:
        return self._mode

    def add_documents_from_text(self, text: str, title: str = "User Document"):
        """Add new documents (only supported in semantic mode)."""
        if not self._initialized:
            self.initialize()
        if isinstance(self._backend, ChromaRetriever) and self._backend.vectorstore:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
            )
            chunks = splitter.create_documents(
                texts=[text],
                metadatas=[{"title": title, "source": "user_upload"}],
            )
            self._backend.vectorstore.add_documents(chunks)
            self._backend.vectorstore.persist()
            return len(chunks)
        logger.warning("Dynamic document add only supported in semantic mode.")
        return 0


# Global singleton instance
rag_pipeline = TelecomRAGPipeline()

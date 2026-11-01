"""Simple keyword search over Markdown notes, using the BM25 ranking method."""

from .bm25 import BM25Index, tokenize

__all__ = ["BM25Index", "tokenize"]
__version__ = "0.1.0"

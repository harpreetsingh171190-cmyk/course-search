"""A small BM25 search index. Standard library only."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase the text and split it into words made of letters and digits."""
    return TOKEN_PATTERN.findall(text.lower())


@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    score: float
    snippet: str


class BM25Index:
    """Ranks documents against a query using BM25.

    k1 controls how much repeated words count, and b controls how much
    long documents are penalized. The defaults are the usual textbook values.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._docs: dict[str, str] = {}
        self._tokens: dict[str, list[str]] = {}
        self._freqs: dict[str, Counter[str]] = {}
        self._doc_freq: Counter[str] = Counter()
        self._total_length = 0

    def __len__(self) -> int:
        return len(self._docs)

    def add(self, doc_id: str, text: str) -> None:
        """Add a document. Adding the same id again replaces the old text."""
        if doc_id in self._docs:
            self._remove(doc_id)
        tokens = tokenize(text)
        self._docs[doc_id] = text
        self._tokens[doc_id] = tokens
        self._freqs[doc_id] = Counter(tokens)
        self._doc_freq.update(set(tokens))
        self._total_length += len(tokens)

    def _remove(self, doc_id: str) -> None:
        old_tokens = self._tokens.pop(doc_id)
        self._doc_freq.subtract(set(old_tokens))
        self._doc_freq += Counter()  # drop words that now have zero count
        self._total_length -= len(old_tokens)
        del self._freqs[doc_id]
        del self._docs[doc_id]

    def _idf(self, term: str) -> float:
        n = len(self._docs)
        df = self._doc_freq.get(term, 0)
        return math.log((n - df + 0.5) / (df + 0.5) + 1)

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        """Return up to `limit` documents, best match first. Empty query gives no results."""
        terms = set(tokenize(query))
        if not terms or not self._docs:
            return []

        avg_len = (self._total_length / len(self._docs)) or 1.0  # avoid dividing by zero
        results: list[SearchResult] = []
        for doc_id, freqs in self._freqs.items():
            doc_len = len(self._tokens[doc_id])
            score = 0.0
            for term in terms:
                tf = freqs.get(term, 0)
                if tf == 0:
                    continue
                norm = tf * (self.k1 + 1) / (
                    tf + self.k1 * (1 - self.b + self.b * doc_len / avg_len)
                )
                score += self._idf(term) * norm
            if score > 0:
                results.append(SearchResult(doc_id, score, self._snippet(doc_id, terms)))

        results.sort(key=lambda r: (-r.score, r.doc_id))
        return results[:limit]

    def _snippet(self, doc_id: str, terms: set[str], width: int = 120) -> str:
        """Return a short piece of the document around the first matching word."""
        text = " ".join(self._docs[doc_id].split())
        lower = text.lower()
        positions = [lower.find(t) for t in terms if t in lower]
        if not positions:
            return text[:width]
        start = max(0, min(positions) - width // 4)
        return text[start : start + width].strip()

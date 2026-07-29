from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
    "were", "will", "with",
    "bạn", "bằng", "các", "cho", "có", "của", "đã", "đang", "được", "giúp",
    "hãy", "khi", "là", "một", "những", "này", "theo", "trong", "từ", "và",
    "về", "với",
}


def _normalized_words(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", (text or "").lower())
    return [
        word
        for word in re.findall(r"[^\W\d_]+", normalized, flags=re.UNICODE)
        if len(word) > 1 and word not in STOPWORDS
    ]


def extract_keywords(text: str = "", max_keywords: int = 8) -> dict[str, Any]:
    limit = max(1, min(int(max_keywords or 8), 20))
    words = _normalized_words(text)
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    return {
        "tool": "extract_keywords",
        "keywords": [
            {"keyword": keyword, "count": count}
            for keyword, count in ranked
        ],
        "total_terms": len(words),
    }

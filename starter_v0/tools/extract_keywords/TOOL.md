---
name: extract_keywords
track: team
kind: local_text_analysis
provider: local_python
requires_env: []
inputs: [text, max_keywords]
outputs: [keywords, total_terms]
side_effect: false
---
# extract_keywords

Extracts the most frequent meaningful keywords from text that the user already
provided or that a previous tool retrieved.

Use this tool when the user explicitly asks for keywords, key terms, or frequent
terms from available text. It does not search the web, fetch a URL, summarize
content, or infer keywords from an article whose text has not been retrieved.

`max_keywords` is clamped to 1–20. Results are sorted by descending frequency
and then alphabetically for deterministic output.

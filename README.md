# course-search

A small, dependency-free search tool for Markdown notes. It ranks documents with **BM25**, the same family of method used by many search engines, and prints the best matches with a short snippet.

[![CI](https://github.com/harpreetsingh171190-cmyk/course-search/actions/workflows/ci.yml/badge.svg)](https://github.com/harpreetsingh171190-cmyk/course-search/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

## Why this project

Search is a common need, and the core idea (scoring words by how rare and how frequent they are) is easy to test. The project uses only the Python standard library, so it has no installation problems and runs fast in CI.

## Quick start

Requires Python 3.11 or newer.

```bash
git clone https://github.com/harpreetsingh171190-cmyk/course-search.git
cd course-search
PYTHONPATH=src python -m course_search "attention mechanism" --folder path/to/notes
```

Example output, searching the course notes in this repository for `quantization bits memory`:

```text
1. 02-scientist.md (score 3.89)
   not seen during training. ## Quantization Quantization stores weights with fewer bits, such as 8-bit or 4-bit, so a mod
```

## Using it in Python

```python
from course_search import BM25Index

index = BM25Index()
index.add("intro.md", "Transformers use attention to weigh tokens.")
index.add("cooking.md", "Boil pasta in salted water.")

for result in index.search("attention", limit=3):
    print(result.doc_id, round(result.score, 2))
```

## How ranking works

- **Term frequency:** a word that appears more often scores higher, but with diminishing returns.
- **Inverse document frequency:** a rare word matters more than a common one.
- **Length normalization:** a long document is not favored just because it is long.

## Running the tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Project layout

```
src/course_search/   the search library and command line tool
tests/               unit tests (no internet needed)
.github/workflows/   CI on Python 3.11 and 3.12
```

## License

Apache 2.0. See [LICENSE](LICENSE).

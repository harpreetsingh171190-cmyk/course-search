from course_search.bm25 import BM25Index, tokenize


def test_tokenize_lowercases_and_splits_on_non_letters():
    assert tokenize("Hello, World! GPT-4") == ["hello", "world", "gpt", "4"]


def test_empty_index_returns_no_results():
    assert BM25Index().search("anything") == []


def test_empty_query_returns_no_results():
    index = BM25Index()
    index.add("a", "some text here")
    assert index.search("   ") == []


def test_document_with_the_word_ranks_first():
    index = BM25Index()
    index.add("transformers", "Attention is the core of transformers.")
    index.add("cooking", "Boil water and add pasta.")
    results = index.search("attention")
    assert [r.doc_id for r in results] == ["transformers"]


def test_rarer_word_scores_higher_than_common_word():
    index = BM25Index()
    index.add("d1", "the model is good")
    index.add("d2", "the model is fast")
    index.add("d3", "the quantization method")
    rare = index.search("quantization")[0].score
    common = index.search("model")[0].score
    assert rare > common


def test_limit_is_respected():
    index = BM25Index()
    for i in range(10):
        index.add(f"doc{i}", "shared word")
    assert len(index.search("shared", limit=3)) == 3


def test_readding_a_document_replaces_it():
    index = BM25Index()
    index.add("doc", "old content about apples")
    index.add("doc", "new content about bananas")
    assert len(index) == 1
    assert index.search("apples") == []
    assert [r.doc_id for r in index.search("bananas")] == ["doc"]


def test_results_are_sorted_best_first():
    index = BM25Index()
    index.add("low", "pasta once")
    index.add("high", "pasta pasta pasta")
    results = index.search("pasta")
    assert [r.doc_id for r in results] == ["high", "low"]
    assert results[0].score >= results[1].score


def test_snippet_contains_the_matching_word():
    index = BM25Index()
    index.add("doc", "A long intro. The key idea is gradient descent for learning.")
    snippet = index.search("gradient")[0].snippet
    assert "gradient" in snippet


def test_document_with_only_empty_text_does_not_crash():
    index = BM25Index()
    index.add("empty", "")
    assert index.search("anything") == []

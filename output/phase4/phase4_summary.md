# Phase 4 Benchmark Summary

## Best Random Split Model

- Model: `tfidf_word_logreg`
- Macro-F1: 0.7259
- Clickbait F1: 0.6429
- Balanced Accuracy: 0.7421

## Models Used For Domain Generalization

- Best Logistic Regression: `tfidf_word_logreg`
  - Vectorizer: `word`
  - Random-test Macro-F1: 0.7259
  - Random-test Clickbait F1: 0.6429
- Best Linear SVM: `tfidf_word_svm`
  - Vectorizer: `word`
  - Random-test Macro-F1: 0.7184
  - Random-test Clickbait F1: 0.6182

## Hardest Source-Held-Out Case

- Model: `tfidf_word_logreg`
- Held-out source: `VnExpress`
- Macro-F1: 0.6288
- Clickbait F1: 0.4444

## Hardest Category-Held-Out Case

- Model: `tfidf_word_svm`
- Held-out category: `Giải trí & Showbiz`
- Macro-F1: 0.5708
- Clickbait F1: 0.6573

## Notes

- Accuracy is reported but should not be used as the main metric.
- Macro-F1 is the primary metric.
- Source/category metadata is not used as model input in the main benchmark.
- Domain-held-out results should be compared against random split results to quantify robustness drop.
